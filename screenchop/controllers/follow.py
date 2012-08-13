#!/usr/bin/env python

'''
follow.py - Controller to subscribe and unsubscribe to tags.

'''

from flask import Flask
from flask import request, session, redirect


from screenchop import config
from screenchop.sessions import requires_auth
from screenchop.models import User

@requires_auth
def follow(user):
    """ Controller for following a user """
    try:
        User.objects(username=session['username']).update_one(add_to_set__following=user)
        return redirect('/u/%s' % user)
        
    except:
        return 'fail'

@requires_auth
def unfollow(user):
    """ Controller for unfollowing a user """
    try:

        User.objects(username=session['username']).update_one(pull__following=user)
        return redirect('/u/%s' % user)
        
    except:
        return 'fail'

