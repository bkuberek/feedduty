# -*- coding: utf-8 -*-
# Copyright © 2013 Bastian Kuberek
import json
import traceback
import logging

from pyramid.events import (
    subscriber,
    NewRequest,
    BeforeRender
    )

from pyramid.response import Response
from pyramid.view import view_config

log = logging.getLogger(__name__)


@subscriber(NewRequest)
def set_api_renderer(event):
    request = event.request

    if request.content_type in ('text/json', 'application/json'):
        request.override_renderer = 'json'

    return True


@subscriber(BeforeRender)
def override_renderer_data(event):
    # import pdb; pdb.set_trace()

    request = event.get('request')

    if request.content_type in ('text/json', 'application/json'):
        if event.has_key('form'):
            # todo: serialize form filds into JSON ?
            del event['form']
    else:
        if event.has_key('result'):
            event['result'] = json.dumps(event['result'], indent=4)


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
