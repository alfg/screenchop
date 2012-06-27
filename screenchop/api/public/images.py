#!/usr/bin/env python

from flask import Flask
from flask import request
from flask import abort, redirect, url_for, jsonify
from flask import render_template

from screenchop.models import *
from screenchop import config
import json

#app = Flask(__name__)

def getMainImages():

    s3ThumbsURL = config.S3_THUMBS_URL
    s3FullURL = config.S3_FULL_URL
    s3MediumURL = config.S3_MEDIUM_URL
    
    post = Post.objects.order_by('-date').limit(config.HOME_MAX_IMAGES)
    
    #Query list of dictionaries for a JSON object
    jsonImageQuery = [
                        {'filename' : s3FullURL + x.filename,
                         'thumbnail' : s3ThumbsURL + x.filename,
                         'large' : s3MediumURL + x.filename,
                         'width' : x.width,
                         'height' : x.height,
                         'caption' : x.caption
                         } for x in post]
    
    return jsonify(images=jsonImageQuery)
