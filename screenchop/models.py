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
    comments = ListField()
    thumbnail = StringField()
    filename = StringField()
    medium = StringField()
    date = StringField()
    rating = FloatField()
    width = IntField()
    height = IntField()
    
class User(Document):
    userid = SequenceField()
    username = StringField(unique=True)
    password = StringField()

