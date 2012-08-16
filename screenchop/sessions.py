import sys, traceback
from functools import wraps

from flask import Flask
from flask import request, redirect, url_for, session, flash
from flask import render_template, jsonify

from flaskext.bcrypt import check_password_hash, generate_password_hash

from screenchop.models import *
from screenchop import config
from screenchop.forms import RegistrationForm, LoginForm
from screenchop.util.invite_codes import InviteCode



def login():
    ''' Login controller when logging in. 'Success' is returned when accepted
    and frontend JS will redirect accordingly if 'Success' is returned. '''
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        
        # Check if user exists, then check if password hash matches.
        try:
            user = User.objects.get(username__iexact=form.username.data)
        except:
            return 'You shall not pass.'
        
        if check_password_hash(user.password, form.password.data) == True:
            session['username'] = user.username
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
        
            c = InviteCode()

            # Check if invite code is valid
            if c.is_valid(form.invite_code.data) == False: 
                error = {"code": ["Invitation code invalid"]}
                return jsonify(errors=error)
        else:
            pass
            
        # Check or create if user does not exist
        #user, created = User.objects.get_or_create(username__exact=form.username.data)
        try:
            user = User.objects.get(username__iexact=form.username.data)
            created = False 
        except:
            user = User(username=form.username.data)
            created = True
        
        # if created == True, then create a password, save and login session
        if created:
            # Set password and save
            user.password = generate_password_hash(form.password.data)
            user.save()

            # If invite-mode on, use invite code
            if config.REGISTRATION_LEVEL == 'invite':
                c = InviteCode()

                # Use code
                c.use_code(form.invite_code.data, form.username.data)

            # Log in user and flash message
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
