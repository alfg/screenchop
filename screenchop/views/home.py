#!/usr/bin/env python

from flask import Flask
from flask import request
from flask import render_template

from screenchop.models import *
from screenchop import config
from screenchop.forms import RegistrationForm, LoginForm

app = Flask(__name__)

def home():
    # Configure S3 Thumbs directory
    s3ThumbsURL = config.S3_THUMBS_URL

    # Configure max images to show on front page
    galleryMaxImages = config.MAX_IMAGES_PER_ROW

    # For registration/login validation
    regForm = RegistrationForm(request.form)
    loginForm = LoginForm(request.form)

    return render_template('main/home.html', s3ThumbsURL=s3ThumbsURL,
                        galleryMaxImages=galleryMaxImages, regForm=regForm, loginForm=loginForm)
    
def uploads():
    '''
    The uploading view
    
    '''
    return render_template('main/uploads.html')
