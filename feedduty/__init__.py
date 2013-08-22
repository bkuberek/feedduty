# -*- coding: utf-8 -*-
# Copyright © 2013 Bastian Kuberek
import datetime
from pyramid.config import Configurator
from pyramid.renderers import JSON
import pyramid.tweens
from pyramid_jinja2 import renderer_factory as jinja2_renderer
from sqlalchemy import engine_from_config

from feedduty.models import (
    DBSession,
    BaseModel,
    )

# __version__ = VERSION = (0, 1, 0, 'dev', 0)
#
#
# def get_version():
#     """ Return the current version"""
#     version = '%s.%s' % (VERSION[0], VERSION[1])
#     if VERSION[2]:
#         version = '%s.%s' % (version, VERSION[2])
#     if VERSION[3:] == ('alpha', 0):
#         version = '%s pre-alpha' % version
#     else:
#         if VERSION[3] != 'final':
#             version = '%s %s %s' % (version, VERSION[3], VERSION[4])
#     return version


def _datetime_adapter(obj, request):
    return obj.isoformat()


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    # configure SQLAlchemy
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    BaseModel.metadata.bind = engine

    # Load pyramid configuration
    config = Configurator(settings=settings)

    # Configure extensions
    config.add_jinja2_search_path("feedduty:templates")

    # tweens (middleware)
    # config.add_tween('feedduty.tweens.timing_tween_factory')
    # config.add_tween('feedduty.tweens.api_response_tween_factory', under=pyramid.tweens.MAIN)

    # Configure renderers
    # Configure JSON renderer to understand certain objects
    json_renderer = JSON()
    json_renderer.add_adapter(datetime.datetime, _datetime_adapter)

    config.add_renderer('json', json_renderer)
    config.add_renderer('.html', jinja2_renderer)

    # Static assets - this should only work in dev, in prod it should be served by web server (nginx?)
    config.add_static_view('static', 'feedduty:static', cache_max_age=3600)

    # API Routing configuration
    config.add_route('api.main', '/api')

    # Catch all route - loads the web app
    config.add_route('app', '/')

    # scan for view handlers
    config.scan('feedduty.views')

    # return a uwsgi compatible app
    return config.make_wsgi_app()


# if __name__ == "__main__":
#     import os
#     import multiprocessing
#     from paste.deploy import appconfig, loadapp
#     from gunicorn.app.pasterapp import paste_server
#
#     iniFile = 'config:development.ini'
#     port = int(os.environ.get("PORT", 8000))
#     workers = multiprocessing.cpu_count() * 2 + 1
#     worker_class = 'gevent'
#
#     app = loadapp(iniFile, relative_to='.')
#     paste_server(app, host='0.0.0.0', port=port, workers=workers, worker_class=worker_class)
