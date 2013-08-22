# -*- coding: utf-8 -*-
# Copyright © 2013 Spotify AB

from psycogreen.gevent import patch_psycopg

bind = '127.0.0.1:8000'

debug = True
workers = 4
worker_class = 'gevent'
timeout = 120
worker_connections = 10
keepalive = 2
log_level = 'DEBUG'

# Enabling daemon-mode will fork-exec processes which will really confuse supervision
daemon = False

# Patch psycopg2 to work with gevent
def pre_fork(server, worker):
    patch_psycopg()
    worker.log.info('Patched psycopg with gevent support')
