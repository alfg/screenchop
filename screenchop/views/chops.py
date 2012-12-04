#!/usr/bin/env python

from flask import Flask
from flask import request, session, redirect, url_for
from flask import render_template, flash


from screenchop.models import *
from screenchop import config
from screenchop.forms import RegistrationForm, LoginForm, EditPost
from screenchop.sessions import *
from screenchop.cache import cache
from screenchop.util import mailer

import boto
from boto.s3.key import Key

app = Flask(__name__)

# Enable/disable tagging. For debugging.
tagging = config.TAGGING_ENABLED

def chop(filename):
    """ The Screenshot "chop" View """
    
    s3ThumbsURL = config.S3_THUMBS_URL
    s3FullURL = config.S3_FULL_URL
    s3MediumURL = config.S3_MEDIUM_URL
    
    try:
        # Query post
        chop = Post.objects.get(filename = filename)
    except:
        return render_template('error_pages/404.html'), 404
    
    # Checking if username in session to check 2 things
    if 'username' in session:
        # Loading user vote data to object
        vote = Vote.objects(username=session['username'], postuid=chop.uid)
        
        # Also checking to see session is owner of the post. If so, then allow
        # tagging. String booleans since that's how the js lib is checking.
        if session['username'] == chop.submitter:
            tagable = 'true'
        else:
            tagable = 'false'
    else:
        # No votes and not taggable if user is not logged in
        vote = []
        tagable = 'false'
    
    # For registration/login wtf validation
    regForm = RegistrationForm(request.form)
    loginForm = LoginForm(request.form)
    editPostForm = EditPost(request.form,
                            caption=chop.caption,
                            tags=chop.tags)

    
    # For image linking, short url sharing.
    fullURL = config.DOMAIN_URL
    shortURL = config.SHORT_DOMAIN_URL
    
    # Calculate total score of post
    score = int(chop.upvotes) - int(chop.downvotes)
    
    return render_template('chops/chop.html', chop=chop, regForm=regForm,
                            loginForm=loginForm, editPostForm=editPostForm,
                            fullURL=fullURL, shortURL=shortURL, score=score,
                            vote=vote, tagging=tagging, tagable=tagable,
                            s3FullURL=s3FullURL, s3MediumURL=s3MediumURL,
                            s3ThumbsURL=s3ThumbsURL)
                            
@requires_auth        
def delete_chop(filename):
    """ Controller to delete a chop post """ 
    
    # Query post
    chop = Post.objects.get(filename = filename)
    
    # User session is the submitter, then delete the post
    # otherwise, redirect with a flash message
    if session['username'] == chop.submitter:
        # Delete MongoDB post
        chop.delete()
        
        # Connect to S3 and delete all key objects
        conn = boto.connect_s3(config.AWS_ACCESS_KEY_ID,
                                 config.AWS_SECRET_ACCESS_KEY)
                                 
        b = conn.get_bucket(config.BUCKET_NAME)
        k = Key(b)
        
        k.key = 'full/' + filename
        b.delete_key(k)
        k.key = 'medium/' + filename
        b.delete_key(k)
        k.key = 'thumbs/' + filename
        b.delete_key(k)
            
    else:
        flash('You are not the submitter')
        return redirect('/c/%s' % filename)
    
    flash('Screenchop deleted')
    return redirect(url_for('home'))

@requires_auth
def update_chop(filename):
    """ Controller to update a chop post """

    # Initiate form for validation
    form = EditPost(request.form)

    # Query post
    chop = Post.objects.get(filename = filename)

    if request.method == 'POST' and form.validate():


        # User session is the submitter, then edit post
        # otherwise, redirect with flash message
        if session['username'] == chop.submitter:
            # Update post
            chop.caption = form.caption.data
            chop.tags = form.tags.data
            chop.save()

        else:
           flash('You are not the submitter of this post')
           return redirect('/c/%s' % filename)

        flash('Screenchop updated')
        return redirect('/c/%s' % filename)
    errors = form.errors
    flash(errors)
    return redirect('/c/%s' % filename) 

def report_chop(filename):
    mailer.report_chop(filename)
    flash('Thank you for reporting this post. A moderator has been notified.')
    return redirect('/c/%s' % filename)

