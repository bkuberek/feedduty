# -*- coding: utf-8 -*-
# Copyright © 2013 Bastian Kuberek

from pyramid.view import view_config


@view_config(route_name='app', renderer='app.html')
def main(request):
    return {}
