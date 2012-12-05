""" star.py - Controller to star and unstar posts/chops."""

import os, sys
from time import strftime

from flask import Flask
from flask import request, session

from screenchop import config
from screenchop.sessions import requires_auth
from screenchop.models import Post, Star 

app = Flask(__name__)

def star():
    """ Get or Create favorite when starred from a post. Ajax request made on custom.js """
    if 'username' not in session:
        return 'not logged in'

    chop = request.form['chop']
    chopObject = Post.objects.get(filename=chop)
    star, created = Star.objects.get_or_create(username=session['username'], postuid=chopObject.uid)
    
    if created:
        Star.objects(username=session['username'],
                postuid=chopObject.uid).update_one(set__starred=True)
        return 'starred'

    elif star.starred == False:
        Star.objects(username=session['username'],
                postuid=chopObject.uid).update_one(set__starred=True)
        return 'starred'

    else:
        Star.objects(username=session['username'],
                        postuid=chopObject.uid).update_one(set__starred=False)
        return 'unstarred'

    print 'Starred: ', star.starred 
