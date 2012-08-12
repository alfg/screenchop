#!/usr/bin/env python

'''
subscriptions.py - Controller to subscribe and unsubscribe to tags.

'''

from flask import Flask
from flask import request, session, redirect


from screenchop import config
from screenchop.sessions import requires_auth
from screenchop.models import User


def subscribe(tag):
    try:
        if 'username' not in session:
            return 'not logged in'
            
        User.objects(username=session['username']).update_one(push__subscriptions=tag)
        return redirect('/tags/%s' % tag)
        
    except:
        return 'fail'
        
def unsubscribe(tag):
    try:
        if 'username' not in session:
            return 'not logged in'
            
        User.objects(username=session['username']).update_one(pull__subscriptions=tag)
        return redirect('/tags/%s' % tag)
        
    except:
        return 'fail'

