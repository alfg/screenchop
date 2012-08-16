#!/usr/bin/env python

from flask import Flask
from flask import request
from flask import abort, redirect, url_for, jsonify
from flask import render_template

from screenchop.models import *
from screenchop import config

import json
import datetime


def userFollowing_json():
    """ JSON API to request followed users from specified user. """
    
    username = request.args.get('user', None)
    
    avatarURL = config.S3_AVATAR_URL
    
    user = User.objects.get(username__iexact=username)
    print user

    #Query list of dictionaries for a JSON object
    jsonUserQuery = [
                        {'username' : user.username,
                        'following': user.following                        
                         }]
    
    return jsonify(user=jsonUserQuery)
