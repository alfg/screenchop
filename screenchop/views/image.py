#!/usr/bin/env python

from flask import Flask
from flask import request, session, redirect, url_for, make_response
from flask import render_template, flash, send_file
import StringIO

from screenchop.models import *
from screenchop import config
from screenchop.forms import RegistrationForm, LoginForm

from screenchop.sessions import *

import boto
from boto.s3.key import Key

app = Flask(__name__)

def image():
    '''
    The image view
    
    '''
    conn = boto.connect_s3(config.AWS_ACCESS_KEY_ID,
                             config.AWS_SECRET_ACCESS_KEY)
                             
    b = conn.get_bucket(config.BUCKET_NAME)

    k = Key(b)

    key = b.get_key('thumbs/00d9b23258574b3485aa8ffe449ccb54')
    #$img_byte_string = key.get_contents_as_string()

    response = make_response(key.get_contents_as_string())
    response.headers['Content-Type'] = 'image/jpeg'

    return response

