# -*- coding: utf-8 -*-
# Copyright © 2013 Bastian Kuberek

import time
from pyramid.settings import asbool
import logging

log = logging.getLogger(__name__)


def timing_tween_factory(handler, registry):
    if asbool(registry.settings.get('do_timing')):
        # if timing support is enabled, return a wrapper
        def timing_tween(request):
            start = time.time()
            try:
                response = handler(request)
            finally:
                end = time.time()
                log.debug('The request took %s seconds' % (end - start))

            return response

        return timing_tween
    # if timing support is not enabled, return the original
    # handler
    return handler


def api_response_tween_factory(handler, registry):
    if True:
        # if timing support is enabled, return a wrapper
        def api_response_tween(request):

            try:
                response = handler(request)
                print response
            finally:
                log.debug('API Response Tween')

            return response

        return api_response_tween
    return handler
