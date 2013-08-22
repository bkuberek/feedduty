# -*- coding: utf-8 -*-
# Copyright © 2013 Bastian Kuberek

from cornice.resource import resource, view

from feedduty.models import (
    DBSession,
    Tag,
    )

from feedduty.serializers import TagJsonSerializer
from feedduty.forms import TagForm

@resource(collection_path='/api/tag', path='/api/tag/{id}')
class TagResource(object):
    def __init__(self, request):
        self.request = request
        self.serializer = TagJsonSerializer()

    @view(renderer='json')
    def collection_get(self):
        """
        List Tags - Only accepts GET requests on the collection URI

        """
        tags = DBSession.query(Tag)

        return {'success': True, 'result': [self.serializer.serialize(d) for d in tags]}

    @view(renderer='json')
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

    @view(renderer='json')
    def get(self):
        """
        Retrieve a tag
        """
        tag = DBSession.query(Tag).get(int(self.request.matchdict['id']))

        return {'success': True, 'result': self.serializer.serialize(tag)}

    @view(renderer='json')
    def put(self):
        """
        Update a tag
        """
        form = TagForm(self.request.POST)
        tag = DBSession.query(Tag).get(int(self.request.matchdict['id']))

        if form.validate():
            # extract values from form and populate the tag instance
            # Since the object already exists in the database, the db session will automatically commit the changes
            form.populate_obj(tag)

            resp = {'success': True, 'result': self.serializer.serialize(tag)}
        else:
            resp = {'success': False, 'errors': {}}

        return resp

    @view(renderer='json')
    def delete(self):
        """
        Delete a tag
        """
        tag = DBSession.query(Tag).get(int(self.request.matchdict['id']))

        # Tell the database to remove the record
        DBSession.delete(tag)

        return {'success': True}
