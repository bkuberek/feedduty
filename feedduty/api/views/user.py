# -*- coding: utf-8 -*-
# Copyright © 2013 Bastian Kuberek

from cornice.resource import resource

from feedduty.models import (
    DBSession,
    User,
    )

from feedduty.api.views import Resource as BaseResource
from feedduty.api.forms import UserForm


@resource(collection_path='/api/user', path='/api/user/{id}')
class UserResource(BaseResource):
    def __init__(self, request):
        BaseResource.__init__(self, request)
        self.model = User
        self.form = UserForm
