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

def home():
    # Configure S3 Thumbs directory
    s3ThumbsURL = config.S3_THUMBS_URL

    # Configure max images to show on front page
    maxPerRow = config.MAX_IMAGES_PER_ROW

    # For registration/login validation
    regForm = RegistrationForm(request.form)
    loginForm = LoginForm(request.form)

    return render_template('main/home.html', s3ThumbsURL=s3ThumbsURL,
                        maxPerRow=maxPerRow, regForm=regForm, loginForm=loginForm)
@requires_auth
def upload():
    '''
    The Upload View
    
    '''

    return render_template('main/upload.html')
    
@requires_auth
def account():
    '''
    The Account View
    
    '''
    user = User.objects.get(username = session['username'])
    form = AccountForm(request.form)
    if request.method == 'POST' and form.validate():
        if check_password_hash(user.password, form.currentpass.data):
            User.objects(username=session['username']).update(set__password=generate_password_hash(form.newpass.data))
            flash('Account updated')
            return redirect(url_for('account'))
        else:
            flash('Current password did not match. Account not updated')
            return redirect(url_for('account'))
        
    return render_template('main/account.html', user=user, form=form)

