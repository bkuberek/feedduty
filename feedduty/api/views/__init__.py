# -*- coding: utf-8 -*-
# Copyright © 2013 Bastian Kuberek
import json
import traceback
import logging

from pyramid.response import Response
from pyramid.view import view_config

log = logging.getLogger(__name__)


class Resource(object):
    def __init__(self, request):
        self.request = request

        if self.request.accept.accepts_html and self.request.method == 'GET':
            self.render_json = False
            self.request.override_renderer = 'content.html'
        else:
            self.render_json = True
            self.request.override_renderer = 'json'


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
