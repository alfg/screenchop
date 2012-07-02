#!/usr/bin/env python

'''
vote.py - Controller to upvote and downvote posts/chops.

'''
import os, sys
from time import strftime

from flask import Flask
from flask import request, session
from flask import abort, redirect, url_for, jsonify
from flask import render_template, flash

from screenchop import config
from screenchop.sessions import requires_auth
from screenchop.models import Post

app = Flask(__name__)

def upvote():
    chop = request.form['chop']
    print chop
    #chop = Post.objects.get(filename='zaf32')

    Post.objects(filename=chop).update_one(inc__upvotes=1)
    return 'upvoted'
    
def downvote():
    chop = request.form['chop']
    print chop
    #chop = Post.objects.get(filename='zaf32')

    Post.objects(filename=chop).update_one(inc__downvotes=1)
    return 'downvoted'
