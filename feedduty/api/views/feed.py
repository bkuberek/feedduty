# -*- coding: utf-8 -*-
# Copyright © 2013 Bastian Kuberek
import json
from cornice.resource import resource

from feedduty.models import (
    DBSession,
    Feed,
    )

from feedduty.api.views import Resource as BaseResource
from feedduty.api.forms import FeedForm

@resource(collection_path='/api/feed', path='/api/feed/{id}')
class FeedResource(BaseResource):
    def __init__(self, request):
        BaseResource.__init__(self, request)
        self.model = Feed
        self.form = FeedForm
