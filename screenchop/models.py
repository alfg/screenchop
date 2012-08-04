#!/usr/bin/env python
'''
MongoDB Models

'''

from mongoengine import *
from screenchop import config

connect(config.MONGO_DATABASE, host=config.MONGO_HOST,
        port=config.MONGO_PORT, username=config.MONGO_USER,
        password=config.MONGO_PASS)

class Post(Document):
    uid = SequenceField()
    title = StringField()
    submitter = StringField()
    caption = StringField()
    tags = ListField()
    thumbnail = StringField()
    filename = StringField()
    medium = StringField()
    date = StringField()
    upvotes = IntField(default=0)
    downvotes = IntField(default=0)
    width = IntField()
    height = IntField()
    
class User(Document):
    userid = SequenceField()
    username = StringField(unique=True)
    password = StringField()
    email = EmailField()
    description = StringField()
    avatar = StringField()

class Vote(Document):
    userid = StringField()
    username = StringField()
    postuid = IntField()
    downvoted = BooleanField(default=False)
    upvoted = BooleanField(default=False)
    
class Tag(Document):
    uid = StringField()
    top = IntField()
    left = IntField()
    width = IntField()
    height = IntField()
    text = StringField()
    submitter = StringField()
    postuid = IntField()
    postfilename = StringField()
    
