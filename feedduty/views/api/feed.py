# -*- coding: utf-8 -*-
# Copyright © 2013 Bastian Kuberek
import json
from cornice.resource import resource, view

from feedduty.models import (
    DBSession,
    Feed,
    )

from feedduty.serializers import FeedJsonSerializer
from feedduty.forms import FeedForm
from pyramid.settings import asbool


@resource(collection_path='/api/feed', path='/api/feed/{id}')
class FeedResource(object):
    def __init__(self, request):
        self.request = request
        self.serializer = FeedJsonSerializer()
        self.render_json = asbool(self.request.content_type in ('text/json', 'application/json'))
        if self.render_json:
            self.request.override_renderer = 'json'

    @view(renderer='api/content.html')
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

    @view(renderer='json')
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

    @view(renderer='api/content.html')
    def get(self):
        """
        Retrieve a feed
        """
        feed = DBSession.query(Feed).get(int(self.request.matchdict['id']))

        json_response = {'success': True, 'result': self.serializer.serialize(feed)}

        if self.render_json:
            resp = json_response
        else:
            # embed the response for the HTML templates
            resp = {'json_response': json.dumps(json_response, indent=2)}
            resp['form'] = FeedForm()

        return resp

    @view(renderer='json')
    def put(self):
        """
        Update a feed
        """
        form = FeedForm(self.request.POST)
        feed = DBSession.query(Feed).get(int(self.request.matchdict['id']))

        if form.validate():
            # extract values from form and populate the feed instance
            # Since the object already exists in the database, the db session will automatically commit the changes
            form.populate_obj(feed)

            resp = {'success': True, 'result': self.serializer.serialize(feed)}
        else:
            resp = {'success': False, 'errors': {}}

        return resp

    @view(renderer='json')
    def delete(self):
        """
        Delete a dashboard
        """
        feed = DBSession.query(Feed).get(int(self.request.matchdict['id']))

        # Delete the feed
        DBSession.delete(feed)

        return {'success': True}
