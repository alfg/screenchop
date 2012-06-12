#!/usr/bin/env python

from flask import Flask
from flask import request
from flask import render_template

from screenchop.models import *
from screenchop import config

app = Flask(__name__)

def home():

    s3ThumbsURL = config.S3_THUMBS_URL
    post = Post.objects.order_by('-date')

    return render_template('main/home.html', post=post, s3ThumbsURL=s3ThumbsURL)
    
def uploads():
    '''
    The uploading view
    
    '''
    return render_template('main/uploads.html')
