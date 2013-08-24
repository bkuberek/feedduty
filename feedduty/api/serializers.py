# -*- coding: utf-8 -*-
# Copyright © 2013 Bastian Kuberek

from feedduty.models import (
    User,
    Feed,
    Tag,
    )
from feedduty.util.json_serializer import JsonSerializer


class UserJsonSerializer(JsonSerializer):
    __object_class__ = User
    __attributes__ = [
        'user_id',
        'username',
        'email',
        'first_name',
        'last_name',
        'last_login',
        'settings',
        # 'feeds',
        # 'tags',
    ]
    __required__ = ['username', 'email']
    __attribute_serializer__ = dict(last_login='date', )


class FeedJsonSerializer(JsonSerializer):
    __object_class__ = Feed
    __attributes__ = [
        'feed_id',
        'user_id',
        'user',
        'name',
        'description',
        'settings',
        'url',
        'settings',
        'created_at',
        'updated_at',
        # 'tags',
    ]
    __required__ = ['user_id', 'name', 'url']
    __attribute_serializer__ = dict(created_at='date', updated_at='date')


class TagJsonSerializer(JsonSerializer):
    __object_class__ = Tag
    __attributes__ = [
        'tag_id',
        'name',
    ]
    __required__ = ['name']
