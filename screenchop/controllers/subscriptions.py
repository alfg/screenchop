#!/usr/bin/env python

'''
subscriptions.py - Controller to subscribe and unsubscribe to tags.

'''

from flask import Flask
from flask import request, session, redirect


from screenchop import config
from screenchop.sessions import requires_auth
from screenchop.models import User

@requires_auth
def subscribe(tag):
    """ Controller for subscribing to tags """
    try:
        User.objects(username=session['username']).update_one(add_to_set__subscriptions=tag)
        return redirect('/tags/%s' % tag)
        
    except:
        return 'fail'

@requires_auth
def unsubscribe(tag):
    """ Controller for unsubscribing to tags """
    try:

        User.objects(username=session['username']).update_one(pull__subscriptions=tag)
        return redirect('/tags/%s' % tag)
        
    except:
        return 'fail'

