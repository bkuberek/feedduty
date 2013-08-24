# -*- coding: utf-8 -*-
# Copyright © 2013 Bastian Kuberek
"""
Forms

Regular forms use WTForms http://wtforms.simplecodes.com/docs/1.0.4/
Model CRUD/search forms use WTForms-Alchemy http://wtforms-alchemy.readthedocs.org/en/latest/
"""
from wtforms import Form
from wtforms_alchemy import model_form_factory
from wtforms.validators import Email, URL
from feedduty.models import (
    DBSession,
    User,
    Feed,
    Tag,
)

# Create a custom ModelForm so that we can add common metadata
BaseModelForm = model_form_factory(Form, strip_string_fields=True, )

# Model Forms
#
# This forms are used to create or edit model instances


class ModelForm(BaseModelForm):
    @classmethod
    def get_session(cls):
        """
        Get the SQLAlchemy database session
        """
        return DBSession


class UserForm(ModelForm):
    class Meta:
        model = User
        exclude = ['last_login',]
        validators = {'email': [Email()]}


class FeedForm(ModelForm):
    class Meta:
        model = Feed
        exclude = ['created_at', 'updated_at']
        validators = {'url': [URL()]}


class TagForm(ModelForm):
    class Meta:
        model = Tag


# Filter Forms
#
# This forms are used to filter an SQLAlchemy query


class ModelSearchForm(ModelForm):
    class Meta:
        all_fields_optional = True
        only_indexed_fields = True
        include_primary_keys = True


class FeedSearchForm(ModelSearchForm):
    class Meta:
        model = Feed
