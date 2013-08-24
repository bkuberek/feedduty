# -*- coding: utf-8 -*-
# Copyright © 2013 Bastian Kuberek
import json
import traceback
import logging

from cornice.resource import resource, view
from feedduty.models import DBSession
from pyramid.httpexceptions import HTTPNotFound
from pyramid.response import Response
from pyramid.view import view_config

log = logging.getLogger(__name__)


class Resource(object):
    model = None
    form = None

    def __init__(self, request):
        self.request = request

        if self.request.accept.accepts_html and self.request.method == 'GET':
            self.render_json = False
            self.request.override_renderer = 'content.html'
        else:
            self.render_json = True
            self.request.override_renderer = 'json'

    @view()
    def collection_get(self):
        """
        List objects - Only accepts GET requests on the collection URI

        """

        collection = DBSession.query(self.model).filter()
        json_response = {'success': True, 'result': [obj.__json__(self.request) for obj in collection]}

        if self.render_json:
            resp = json_response
        else:
            # embed the response for the HTML templates
            resp = {'json_response': json.dumps(json_response, indent=2), 'form': self.form()}

        return resp

    @view()
    def collection_post(self):
        """
        Create new object - Only accepts POST requests on the collection URI
        """
        form = self.form(self.request.POST)
        obj = self.model()

        if form.validate():
            # extract values from form and populate the feed instance
            form.populate_obj(obj)

            # Save the feed to the database
            DBSession.add(obj)

            resp = {'success': True, 'result': obj}
        else:
            resp = {'success': False, 'errors': {}}

        return resp

    @view()
    def get(self):
        """
        Retrieve an object
        """
        obj = DBSession.query(self.model).get(int(self.request.matchdict['id']))
        if not obj:
            raise HTTPNotFound()

        json_response = {'success': True, 'result': obj.__json__(self.request)}

        if self.render_json:
            resp = json_response
        else:
            # embed the response for the HTML templates
            resp = {'json_response': json.dumps(json_response, indent=2)}
            resp['form'] = self.form(obj=obj)

        return resp

    @view()
    def put(self):
        """
        Update an object
        """
        form = self.form(self.request.POST)
        obj = DBSession.query(self.model).get(int(self.request.matchdict['id']))
        if not obj:
            raise HTTPNotFound()

        if form.validate():
            # extract values from form and populate the feed instance
            # Since the object already exists in the database, the db session will automatically commit the changes
            form.populate_obj(obj)

            resp = {'success': True, 'result': obj.__json__(self.request)}
        else:
            resp = {'success': False, 'errors': {}}

        return resp

    @view()
    def delete(self):
        """
        Delete an object
        """
        obj = DBSession.query(self.model).get(int(self.request.matchdict['id']))
        if not obj:
            raise HTTPNotFound()

        # Delete the feed
        DBSession.delete(obj)

        return {'success': True}


@view_config(route_name='api_main', renderer='json')
def main(request):
    return {
        'endpoints': [
            {'name': 'feed', 'uri': '/api/feed'},
            {'name': 'tag', 'uri': '/api/tag'},
            {'name': 'user', 'uri': '/api/user'},
        ]
    }


@view_config(context=Exception)
def failed_validation(exc, request):
    response = Response(json.dumps({'success': False, 'error': str(exc)}))
    response.status_int = 500

    log.error(traceback.format_exc())

    return response
