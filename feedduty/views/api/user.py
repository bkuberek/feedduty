# -*- coding: utf-8 -*-
# Copyright © 2013 Bastian Kuberek
import json

from cornice.resource import resource, view

from feedduty.models import (
    DBSession,
    User,
    )

from feedduty.serializers import UserJsonSerializer
from feedduty.forms import UserForm
from pyramid.settings import asbool


@resource(collection_path='/api/user', path='/api/user/{id}')
class UserResource(object):
    def __init__(self, request):
        self.request = request
        self.serializer = UserJsonSerializer()
        self.render_json = asbool(self.request.content_type in ('text/json', 'application/json'))
        if self.render_json:
            self.request.override_renderer = 'json'

    @view(renderer='json')
    def collection_get(self):
        """
        List Users - Only accepts GET requests on the collection URI

        """
        users = DBSession.query(User)

        json_response = {'success': True, 'result': [self.serializer.serialize(u) for u in users]}

        if self.render_json:
            resp = json_response
        else:
            # embed the response for the HTML templates
            resp = {'json_response': json.dumps(json_response, indent=2)}
            resp['form'] = UserForm()

        return resp

    @view(renderer='json')
    def collection_post(self):
        """
        Create new User - Only accepts POST requests on the collection URI
        """
        form = UserForm(self.request.POST)
        user = User()

        if form.validate():
            # extract values from form and populate the user instance
            form.populate_obj(user)

            # Save the user to the database
            DBSession.add(user)

            resp = {'success': True, 'result': self.serializer.serialize(user)}
        else:
            resp = {'success': False, 'errors': {}}

        return resp

    @view(renderer='json')
    def get(self):
        """
        Retrieve a user
        """
        user = DBSession.query(User).get(int(self.request.matchdict['id']))

        json_response = {'success': True, 'result': self.serializer.serialize(user)}

        if self.render_json:
            resp = json_response
        else:
            # embed the response for the HTML templates
            resp = {'json_response': json.dumps(json_response, indent=2)}
            resp['form'] = UserForm()

        return resp

    @view(renderer='json')
    def put(self):
        """
        Update a user
        """
        form = UserForm(self.request.POST)
        user = DBSession.query(User).get(int(self.request.matchdict['id']))

        if form.validate():
            # extract values from form and populate the user instance
            # Since the object already exists in the database, the db session will automatically commit the changes
            form.populate_obj(user)

            resp = {'success': True, 'result': self.serializer.serialize(user)}
        else:
            resp = {'success': False, 'errors': {}}

        return resp

    @view(renderer='json')
    def delete(self):
        """
        Delete a user
        """
        user = DBSession.query(User).get(int(self.request.matchdict['id']))

        # Tell the database to remove the record
        DBSession.delete(user)

        return {'success': True}
