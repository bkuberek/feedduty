# -*- coding: utf-8 -*-
# Copyright © 2013 Bastian Kuberek
"""
Feed Duty SQLAlchemy Models

"""
from datetime import datetime
import json

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Unicode,
    DateTime,
    )

from sqlalchemy.types import (
    TEXT,
    TypeDecorator,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
BaseModel = declarative_base(name='BaseModel')


class JSONEncodedDict(TypeDecorator):
    """
    Represents an immutable structure as a json-encoded string.
        Usage::
            JSONEncodedDict(length, collation, convert_unicode, unicode_error, _warn_on_bytestring)
    """
    impl = TEXT

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value

    def __repr__(self):
        return "JSONEncodedDict()"


class User(BaseModel):
    """

    """
    __tablename__ = 'users'

    #: The User ID - auto incrementing primary key - not associated with Spotify user id
    user_id = Column(Integer, primary_key=True)

    #: User's username - correlates to the uid in LDAP
    username = Column(Unicode(60), unique=True)

    #: User's email - correlates to the mail in LDAP
    email = Column(Unicode(60), unique=True)

    #: User's first name - correlates to the give_name in LDAP
    first_name = Column(Unicode(60))

    #: User's last name - correlates to the sn in LDAP
    last_name = Column(Unicode(60))

    #: user password
    password = Column(String(255))

    #: Last time when the user logged in
    last_login = Column(DateTime, nullable=True)

    #: a dictionary containing user settings
    settings = Column(JSONEncodedDict, default={})

    #: Collection of user's feeds
    feeds = relationship("Feed",backref='user', cascade="all, delete, delete-orphan", passive_deletes=True)

    #: a collection of Tag instances
    tags = relationship("UserTagLookup")

    def __repr__(self):
        return "<User(username='%s', email='%s')>" % (self.username, self.email)

    def __json__(self, request):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'settings': self.settings,
            'feeds': [f.feed_id for f in self.feeds],
            'tags': [t.tag_id for t in self.tags],
        }


class Feed(BaseModel):
    """

    """
    __tablename__ = 'feeds'

    #: auto incrementing primary key
    feed_id = Column(Integer, primary_key=True)

    #: User id
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'))

    #: name given to a widget, if NULL, it will display data_source.title
    name = Column(Unicode(60), nullable=True)

    #: Text describing the widget - if NULL, it will display data_source.description
    description = Column(Unicode, nullable=True)

    #: a dictionary containing feed settings
    settings = Column(JSONEncodedDict, default={})

    #: Feed URL
    url = Column(Unicode(255))

    #: DateTime when created -  needs to be set in the constructor
    created_at = Column(DateTime)

    #: DateTime when updated -  needs to be set by application logic
    updated_at = Column(DateTime)

    #: a collection of Tag instances
    tags = relationship("FeedTagLookup", backref='feeds', cascade="all, delete, delete-orphan", passive_deletes=True)

    def __repr__(self):
        return "<Feed(user_id=%s, name='%s', url='%s')>" % (self.user_id, self.name, self.url)

    def __init__(self):
        BaseModel.__init__(self)
        self.created_at = datetime.now()

    def __json__(self, request):
        return {
            'feed_id': self.feed_id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'settings': self.settings,
            'url': self.url,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'tags': [t.tag_id for t in self.tags],
        }


class Tag(BaseModel):
    """
    Tags are used to organize feeds.
    """
    __tablename__ = 'tags'

    #: User id
    tag_id = Column(Integer, primary_key=True)

    #: Tag name
    name = Column(Unicode(60), unique=True)

    #: a collection of Tag instances
    # feeds = relationship("FeedTagLookup", backref='tags')

    def __repr__(self):
        return "<Tag(tag_id=%s, name='%s')>" % (self.tag_id, self.name)

    def __json__(self, request):
        return {
            'tag_id': self.tag_id,
            'name': self.name,
        }


class FeedTagLookup(BaseModel):
    """
    Lookup table for Feed and Tag
    """
    __tablename__ = 'feed_tag_lookup'

    #: ID to referenced Feed - together with tag_id form the primary_key
    feed_id = Column(Integer, ForeignKey('feeds.feed_id', ondelete='CASCADE'), primary_key=True)

    #: ID to referenced Tag - together with feed_id form the primary_key
    tag_id = Column(Integer, ForeignKey('tags.tag_id', ondelete='CASCADE'), primary_key=True)

    #: Instance of related Tag
    # tag = relationship("Tag", backref="feed_tag_lookup")


class UserTagLookup(BaseModel):
    """
    Lookup table for User and Tag
    """
    __tablename__ = 'user_tag_lookup'

    #: ID to referenced User - together with tag_id form the primary_key
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)

    #: ID to referenced Tag - together with user_id form the primary_key
    tag_id = Column(Integer, ForeignKey('tags.tag_id', ondelete='CASCADE'), primary_key=True,)

    #: Instance of related Tag
    # tag = relationship("Tag", backref="feed_tag_lookup")
