from flask import Flask
from flask import request, redirect, url_for, session
from flask import render_template

from flaskext.bcrypt import check_password_hash, generate_password_hash

from screenchop.models import *
from screenchop import config

import sys, traceback



def login():
    ''' Login controller when logging in. 'Success' is returned when accepted
    and frontend JS will redirect accordingly if 'Success' is returned. '''
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        
        # Check if user exists, then check if password hash matches.
        try:
            user = User.objects.get(username=username)
        except:
            return 'You shall not pass.'
        
        if check_password_hash(user.password, password) == True:
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
    ''' Registration controller. Checks and validates if user exists, passwords
    match, and if password/user are populated at all. When accepting registration,
    the user is redirected from JS frontend when 'Success' is returned.'''
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        passwordVerified = request.form['verify']
        
        try:
            user = User.objects(username=username).first()
            
            # If user does not exist and passwords are validated.
            if user == None and password != '' and password == passwordVerified:
            
                user = User(userid=User.objects.count() + 1,
                            username=username,
                            password=generate_password_hash(password))
                user.save()
                session['username'] = username
                return 'Success'
                
            elif user == None and password != passwordVerified:
                return 'Passwords do not match.'

            elif user != None and password == passwordVerified:
                return 'Username already exists.'
                
            elif password == '':
                return 'Please fill out a password.'
                
            else:
                return 'Something went wrong.'
        except:
            traceback.print_exc(file=sys.stdout)
            return 'Error'

        
    return 'Successss'
