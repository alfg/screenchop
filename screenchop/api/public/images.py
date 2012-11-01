#!/usr/bin/env python

from flask import Flask
from flask import request
from flask import abort, redirect, url_for, jsonify
from flask import render_template

from screenchop.models import *
from screenchop.util import ranking
from screenchop import config
from screenchop.cache import cache

import json
import datetime

def getMainImages():
    """ JSON API to request image data in a JSON request. Used mainly for the
    galleries on front and tags pages. """
    
    user = request.args.get('user', None)
    sortType = request.args.get('sort')
    page = request.args.get('page', 0)
    tag = request.args.get('tag', None)
    time = request.args.get('t', None)
    showFollowing = request.args.get('showFollowing', None)
    
    s3ThumbsURL = config.S3_THUMBS_URL
    s3FullURL = config.S3_FULL_URL
    s3MediumURL = config.S3_MEDIUM_URL
    
    # Set time range to query
    if time == 'hour':
        timerange = datetime.datetime.today() - datetime.timedelta(hours=1)
    elif time == '24h':
        timerange = datetime.datetime.today() - datetime.timedelta(hours=24)
    elif time == '7d':
        timerange = datetime.datetime.today() - datetime.timedelta(days=7)
    elif time == '30d':
        timerange = datetime.datetime.today() - datetime.timedelta(days=30)
    elif time == 'all':
        timerange = datetime.datetime.today() - datetime.timedelta(days=99999)
    else:
        timerange = datetime.datetime.today() - datetime.timedelta(days=99999)
        
    # Front page
    if user == 'all' and tag == 'all':
    
        if sortType == 'new':
            post = Post.objects[int(page):int(page) +
                    config.HOME_MAX_IMAGES].order_by('-date').limit(config.HOME_MAX_IMAGES)

        elif sortType == 'top':
            post = Post.objects[int(page):int(page)
                    + config.HOME_MAX_IMAGES](date__gt=timerange) \
                            .order_by('-upvotes').limit(config.HOME_MAX_IMAGES)

        elif sortType == 'hot':
            post = Post.objects[int(page):int(page)
                    + config.HOME_MAX_IMAGES](date__gt=timerange) \
                            .order_by('-rank').limit(config.HOME_MAX_IMAGES)

        else:
            post = Post.objects[int(page):int(page)
                    + config.HOME_MAX_IMAGES].order_by('-date')
            

    # /tags/<tag> page
    elif user == 'all' and tag != 'all':
    
        if sortType == 'new':
            post = Post.objects[int(page):int(page) +
                    config.HOME_MAX_IMAGES](tags=tag).order_by('-date') \
                            .limit(config.HOME_MAX_IMAGES)

        elif sortType == 'top':
            post = Post.objects[int(page):int(page) +
                    config.HOME_MAX_IMAGES](tags=tag,
                                    date__gt=timerange).order_by('-upvotes').limit(config.HOME_MAX_IMAGES)

        else:
            post = Post.objects[int(page):int(page) + config.HOME_MAX_IMAGES](tags=tag).order_by('-date')
            

    # /following page
    elif user and showFollowing == 'true':

        queryUser = User.objects.get(username__iexact=user)
        followingList = queryUser.following
    
        if sortType == 'new':
            post = Post.objects[int(page):int(page) +
                    config.HOME_MAX_IMAGES](submitter__in=followingList) \
                            .order_by('-date').limit(config.HOME_MAX_IMAGES)

        elif sortType == 'top':
            post = Post.objects[int(page):int(page) +
                    config.HOME_MAX_IMAGES](submitter__in=followingList,
                                            date__gt=timerange) \
                        .order_by('-upvotes').limit(config.HOME_MAX_IMAGES)

        else:
            post = Post.objects[int(page):int(page) +
                    config.HOME_MAX_IMAGES](submitter__in=followingList).order_by('-date')


    else:
        if sortType == 'new':
            post = Post.objects(submitter__iexact=user) \
                    .order_by('-date').limit(config.HOME_MAX_IMAGES)

        elif sortType == 'top':
            post = Post.objects(submitter__iexact=user) \
                    .order_by('-upvotes').limit(config.HOME_MAX_IMAGES)

        else:
            post = Post.objects(submitter__iexact=user)[int(page):int(page) +
                    config.HOME_MAX_IMAGES].order_by('-date')

    
    #Query list of dictionaries for a JSON object
    jsonImageQuery = [
                        {'filename' : x.filename,
                         'thumbnail' : s3ThumbsURL + x.filename,
                         'large' : s3MediumURL + x.filename,
                         'width' : x.width,
                         'height' : x.height,
                         'caption' : x.caption,
                         'upvotes' : x.upvotes,
                         'downvotes' : x.downvotes,
                         'score' : x.upvotes - x.downvotes,
                         'tags' : x.tags,
                         'submitter' : x.submitter,
                         'submitted' : str(x.date),
                         'rank' : x.rank
                         } for x in post]
    
    return jsonify(images=jsonImageQuery)
