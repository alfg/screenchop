#!/usr/bin/env python
""" MongoDB Models """

from mongoengine import *
from screenchop import config
import datetime

connect(config.MONGO_DATABASE, 
        host=config.MONGO_HOST,
        port=config.MONGO_PORT, 
        username=config.MONGO_USER,
        password=config.MONGO_PASS)

class Post(Document):
    uid = SequenceField()
    submitter = StringField(required=True)
    caption = StringField(max_length=200)
    tags = ListField(StringField(max_length=15))
    filename = StringField(max_length=30)
    date = DateTimeField(default=datetime.datetime.now)
    upvotes = IntField(default=0)
    downvotes = IntField(default=0)
    width = IntField(required=True)
    height = IntField(required=True)

    meta = {
        'indexes': ['uid', 'filename']
        }
    
class User(Document):
    userid = SequenceField()
    username = StringField(required=True, unique=True, max_length=30)
    password = StringField(required=True, max_length=60)
    email = EmailField(max_length=60)
    description = StringField(max_length=200)
    avatar = StringField(max_length=100)
    subscriptions = ListField(StringField(max_length=50))
    following = ListField(StringField(max_length=60))

    meta = {
        'indexes': ['userid', 'username', 'email']
        }

class Vote(Document):
    username = StringField(required=True, max_length=60)
    postuid = IntField(required=True)
    downvoted = BooleanField(default=False)
    upvoted = BooleanField(default=False)

    meta = {
        'indexes': ['username', 'postuid']
        }
    
class Tag(Document):
    uid = StringField(required=True)
    top = IntField(required=True)
    left = IntField(required=True)
    width = IntField(required=True)
    height = IntField(required=True)
    text = StringField(max_length=60)
    submitter = StringField(max_length=60)
    postuid = IntField(required=True)
    postfilename = StringField(required=True)

    meta = {
        'indexes': ['uid', 'postuid', 'postfilename']
        }
    
class Invite_code(Document):
    code = StringField(required=True)
    date_used = StringField()
    used_by = StringField()
    valid = BooleanField(default=True)

    meta = {
        'indexes': ['code', 'used_by']
        }
    
class Tag_freq(Document):
    tag = StringField(required=True)
    freq = IntField()

    meta = {
        'indexes': ['tag']
        }
