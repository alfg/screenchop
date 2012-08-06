import sys, traceback
from functools import wraps
from time import strftime

from flask import Flask
from flask import request, redirect, url_for, session, flash
from flask import render_template, jsonify

from flaskext.bcrypt import check_password_hash, generate_password_hash

from screenchop.models import *
from screenchop import config
from screenchop.forms import RegistrationForm, LoginForm



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
            session['username'] = form.username.data
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
    
        # Code to support if invite registration mode is enabled.
        if config.REGISTRATION_LEVEL == 'invite':
        
            # Check if invite code is valid
            if checkInviteCode(form.invite_code.data, form.username.data) != 'success':
                error = {"code": ["Invitation code invalid"]}
                return jsonify(errors=error)
        else:
            pass
            
        # Check or create if user does not exist
        user, created = User.objects.get_or_create(username=form.username.data)
        
        # if created == True, then create a password, save and login session
        if created:
            user.password = generate_password_hash(form.password.data)
            user.save()
            session['username'] = form.username.data
            flash('Thanks for registering!')
            return 'Success'
        else:
            error = {"duplicate": ["Please choose another username"]}
            return jsonify(errors=error)
            


    # Go home if called via GET request directly.
    elif request.method == 'GET':
        return redirect(url_for('home'))

    # Return POST errors in json
    return jsonify(errors=form.errors)

def checkInviteCode(code, user):
    ''' If REGISTRATION_LEVEL is set to 'invite', then this code will be run to
    check if invite code exists and/or is valid. If code is valid, then
    invalidate code after being used. '''
    
    try:
        # Query code
        checkCode = Invite_code.objects.get(code=code)

        # Check if code has been used. Fail if so.
        if checkCode.valid == False:
            return 'fail'
        
        # Invalidate code in DB with a timestamp and user recorded
        checkCode.valid = False
        checkCode.date_used = strftime("%Y-%m-%d_%H-%M-%S")
        checkCode.used_by = user
                  
        checkCode.save()
        
        return 'success'
    except:
        
        # Fail if does not exist exception
        return 'fail'


"""
@requires_auth
Checks if session exists. If not, then denies access to requested page.
Must use @requires_auth before each view function to restrict access.

"""

def deny_access():
    """Sends a 401 response that enables basic auth"""
    flash('You must login first.')
    return redirect(url_for('home'))

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not "username" in session:
            return deny_access()
        return f(*args, **kwargs)
    return decorated
