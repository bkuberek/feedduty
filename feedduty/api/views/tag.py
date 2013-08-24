# -*- coding: utf-8 -*-
# Copyright © 2013 Bastian Kuberek
import json

from cornice.resource import resource, view

from feedduty.models import (
    DBSession,
    Tag,
    )

from feedduty.api.views import Resource as BaseResource
from feedduty.api.serializers import TagJsonSerializer
from feedduty.api.forms import TagForm
from pyramid.httpexceptions import HTTPNotFound


@resource(collection_path='/api/tag', path='/api/tag/{id}')
class TagResource(BaseResource):
    def __init__(self, request):
        BaseResource.__init__(self, request)
        self.serializer = TagJsonSerializer()

    @view()
    def collection_get(self):
        """
        List Tags - Only accepts GET requests on the collection URI

        """
        tags = DBSession.query(Tag)

        json_response = {'success': True, 'result': [self.serializer.serialize(t) for t in tags]}

        if self.render_json:
            resp = json_response
        else:
            # embed the response for the HTML templates
            resp = {'json_response': json.dumps(json_response, indent=2)}
            resp['form'] = TagForm()

        return resp

    @view()
    def collection_post(self):
        """
        Create new Tag - Only accepts POST requests on the collection URI
        """
        form = TagForm(self.request.POST)
        tag = Tag()

        if form.validate():
            # extract values from form and populate the tag instance
            form.populate_obj(tag)

            # Save the tag to the database
            DBSession.add(tag)

            resp = {'success': True, 'result': self.serializer.serialize(tag)}
        else:
            resp = {'success': False, 'errors': {}}

        return resp

    @view()
    def get(self):
        """
        Retrieve a tag
        """
        tag = DBSession.query(Tag).get(int(self.request.matchdict['id']))
        if not tag:
            raise HTTPNotFound()

        json_response = {'success': True, 'result': self.serializer.serialize(tag)}

        if self.render_json:
            resp = json_response
        else:
            # embed the response for the HTML templates
            resp = {'json_response': json.dumps(json_response, indent=2)}
            resp['form'] = TagForm()

        return resp

    @view()
    def put(self):
        """
        Update a tag
        """
        form = TagForm(self.request.POST)
        tag = DBSession.query(Tag).get(int(self.request.matchdict['id']))
        if not tag:
            raise HTTPNotFound()

        if form.validate():
            # extract values from form and populate the tag instance
            # Since the object already exists in the database, the db session will automatically commit the changes
            form.populate_obj(tag)

            resp = {'success': True, 'result': self.serializer.serialize(tag)}
        else:
            resp = {'success': False, 'errors': {}}

        return resp

    @view()
    def delete(self):
        """
        Delete a tag
        """
        tag = DBSession.query(Tag).get(int(self.request.matchdict['id']))
        if not tag:
            raise HTTPNotFound()

        # Tell the database to remove the record
        DBSession.delete(tag)

        return {'success': True}
