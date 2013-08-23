# -*- coding: utf-8 -*-
# Copyright © 2013 Bastian Kuberek
import json
import traceback
import logging

from pyramid.response import Response
from pyramid.view import view_config

log = logging.getLogger(__name__)


@view_config(route_name='api.main', renderer='json')
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
