#!/usr/bin/env python

from flask import Flask
from flask import request, session, redirect, url_for
from flask import render_template, flash

from flaskext.bcrypt import check_password_hash, generate_password_hash

from screenchop.models import *
from screenchop import config
from screenchop.forms import RegistrationForm, LoginForm, AccountForm

from screenchop.sessions import *

app = Flask(__name__)

def user(username):
    # Configure S3 Thumbs directory
    s3ThumbsURL = config.S3_THUMBS_URL

    # Configure max images to show on front page
    maxPerRow = config.MAX_IMAGES_PER_ROW
    pageIncr = config.HOME_MAX_IMAGES # Amount of images to increment/paginate

    # For registration/login validation
    regForm = RegistrationForm(request.form)
    loginForm = LoginForm(request.form)
    
    try:
        user = User.objects.get(username=username)
    except:
        return render_template('error_pages/404.html'), 404
        
    chops = Post.objects(submitter=username)
    
    # Calculate total score by adding all upvotes subtracted by all downvotes
    upvotes = 0
    downvotes = 0
    
    for n in chops:
        upvotes = upvotes + n.upvotes
        downvotes = downvotes + n.downvotes
    score = upvotes - downvotes
    
    return render_template('main/user.html', s3ThumbsURL=s3ThumbsURL,
                        maxPerRow=maxPerRow, regForm=regForm, loginForm=loginForm,
                        pageIncr=pageIncr, user=user, score=score)


