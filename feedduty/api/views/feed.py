# -*- coding: utf-8 -*-
# Copyright © 2013 Bastian Kuberek
import json
from cornice.resource import resource, view

from feedduty.models import (
    DBSession,
    Feed,
    )

from feedduty.api.views import Resource as BaseResource
from feedduty.api.serializers import FeedJsonSerializer
from feedduty.api.forms import FeedForm
from pyramid.httpexceptions import HTTPNotFound


@resource(collection_path='/api/feed', path='/api/feed/{id}')
class FeedResource(BaseResource):
    def __init__(self, request):
        BaseResource.__init__(self, request)
        self.serializer = FeedJsonSerializer()

    @view()
    def collection_get(self):
        """
        List feeds - Only accepts GET requests on the collection URI

        """

        feeds = DBSession.query(Feed).filter()
        json_response = {'success': True, 'result': [self.serializer.serialize(f) for f in feeds]}

        if self.render_json:
            resp = json_response
        else:
            # embed the response for the HTML templates
            resp = {'json_response': json.dumps(json_response, indent=2)}
            resp['form'] = FeedForm()

        return resp

    @view()
    def collection_post(self):
        """
        Create new Feed - Only accepts POST requests on the collection URI
        """
        form = FeedForm(self.request.POST)
        feed = Feed()

        if form.validate():
            # extract values from form and populate the feed instance
            form.populate_obj(feed)

            # Save the feed to the database
            DBSession.add(feed)

            resp = {'success': True, 'result': self.serializer.serialize(feed)}
        else:
            resp = {'success': False, 'errors': {}}

        return resp

    @view()
    def get(self):
        """
        Retrieve a feed
        """
        feed = DBSession.query(Feed).get(int(self.request.matchdict['id']))
        if not feed:
            raise HTTPNotFound()

        json_response = {'success': True, 'result': self.serializer.serialize(feed)}

        if self.render_json:
            resp = json_response
        else:
            # embed the response for the HTML templates
            resp = {'json_response': json.dumps(json_response, indent=2)}
            resp['form'] = FeedForm(obj=feed)

        return resp

    @view()
    def put(self):
        """
        Update a feed
        """
        form = FeedForm(self.request.POST)
        feed = DBSession.query(Feed).get(int(self.request.matchdict['id']))
        if not feed:
            raise HTTPNotFound()

        if form.validate():
            # extract values from form and populate the feed instance
            # Since the object already exists in the database, the db session will automatically commit the changes
            form.populate_obj(feed)

            resp = {'success': True, 'result': self.serializer.serialize(feed)}
        else:
            resp = {'success': False, 'errors': {}}

        return resp

    @view()
    def delete(self):
        """
        Delete a dashboard
        """
        feed = DBSession.query(Feed).get(int(self.request.matchdict['id']))
        if not feed:
            raise HTTPNotFound()

        # Delete the feed
        DBSession.delete(feed)

        return {'success': True}
