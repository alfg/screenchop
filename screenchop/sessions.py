from flask import Flask
from flask import request, redirect, url_for, session, flash
from flask import render_template, jsonify

from flaskext.bcrypt import check_password_hash, generate_password_hash

from screenchop.models import *
from screenchop import config
from screenchop.forms import RegistrationForm, LoginForm

import sys, traceback


def login():
    ''' Login controller when logging in. 'Success' is returned when accepted
    and frontend JS will redirect accordingly if 'Success' is returned. '''
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        
        # Check if user exists, then check if password hash matches.
        try:
            user = User.objects.get(username=form.username.data)
        except:
            return 'You shall not pass.'
        
        if check_password_hash(user.password, form.password.data) == True:
            session['username'] = username
        else:
            return 'You shall not pass.'
        
        return 'Success'
        
    # Go home if called via GET request directly.
    return redirect(url_for('home'))


def logout():
    ''' Remove username from session if exists. '''
    session.pop('username', None)
    return redirect(url_for('home'))
    
def register():
    ''' Registration controller. Checks and validates registration form. 
    When accepting registration, the user is redirected from JS frontend
    when 'Success' is returned.'''

    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():

        user = User(userid=User.objects.count() + 1,
                    username=form.username.data,
                    password=generate_password_hash(form.password.data))
        user.save()
        session['username'] = form.username.data
        print 'user created', user

        return 'Success'

    # Go home if called via GET request directly.
    elif request.method == 'GET':
        return redirect(url_for('home'))

    # Return POST errors in json
    return jsonify(errors=form.errors)

