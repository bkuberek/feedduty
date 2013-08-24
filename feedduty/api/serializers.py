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
        'feeds',
        'tags',
    ]
    __required__ = ['username', 'email']
    __attribute_serializer__ = dict(last_login='date', feeds='feeds', tags='tags')

    feedSerializer = None
    tagSerializer = None

    def getFeedSerializer(self):
        if not self.feedSerializer:
            self.feedSerializer = FeedJsonSerializer()
        return self.feedSerializer

    def getTagSerializer(self):
        if not self.tagSerializer:
            self.tagSerializer = TagJsonSerializer()
        return self.tagSerializer

    def __init__(self):
        self.serializers['feeds'] = {
            'serialize': lambda feeds: [self.getFeedSerializer().serialize(f) for f in feeds],
            'deserialize': lambda feeds: [self.getFeedSerializer().deserialize(f) for f in feeds]
        }

        self.serializers['tags'] = {
            'serialize': lambda tags: [self.getTagSerializer().serialize(t) for t in tags],
            'deserialize': lambda tags: [self.getTagSerializer().deserialize(t) for t in tags]
        }


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
        'tags',
    ]
    __required__ = ['user_id', 'name', 'url']
    __attribute_serializer__ = dict(created_at='date', updated_at='date', users='users', tags='tags')

    userSerializer = None
    tagSerializer = None

    def getUserSerializer(self):
        if not self.userSerializer:
            self.userSerializer = UserJsonSerializer()
        return self.userSerializer

    def getTagSerializer(self):
        if not self.tagSerializer:
            self.tagSerializer = TagJsonSerializer()
        return self.tagSerializer

    def __init__(self):

        self.serializers['users'] = {
            'serialize': lambda users: [self.getUserSerializer().serialize(u) for u in users],
            'deserialize': lambda users: [self.getUserSerializer().deserialize(u) for u in users]
        }

        self.serializers['tags'] = {
            'serialize': lambda tags: [self.getTagSerializer().serialize(t) for t in tags],
            'deserialize': lambda tags: [self.getTagSerializer().deserialize(t) for t in tags]
        }


class TagJsonSerializer(JsonSerializer):
    __object_class__ = Tag
    __attributes__ = [
        'tag_id',
        'name',
    ]
    __required__ = ['name']
    __attribute_serializer__ = dict(feeds='feeds')

    feedSerializer = None

    def getFeedSerializer(self):
        if not self.feedSerializer:
            self.feedSerializer = FeedJsonSerializer()
        return self.feedSerializer

    def __init__(self):
        self.serializers['feeds'] = {
            'serialize': lambda feeds: [self.getFeedSerializer().serialize(f) for f in feeds],
            'deserialize': lambda feeds: [self.getFeedSerializer().deserialize(f) for f in feeds]
        }
