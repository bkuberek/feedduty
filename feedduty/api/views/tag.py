# -*- coding: utf-8 -*-
# Copyright © 2013 Bastian Kuberek

from cornice.resource import resource

from feedduty.models import (
    DBSession,
    Tag,
    )

from feedduty.api.views import Resource as BaseResource
from feedduty.api.forms import TagForm


@resource(collection_path='/api/tag', path='/api/tag/{id}')
class TagResource(BaseResource):
    def __init__(self, request):
        BaseResource.__init__(self, request)
        self.model = Tag
        self.form = TagForm
