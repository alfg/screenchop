#!/usr/bin/env python

from flask import Flask
from flask import request, session, redirect, url_for
from flask import render_template, flash


from screenchop.models import *
from screenchop import config
from screenchop.forms import RegistrationForm, LoginForm

from screenchop.sessions import *

import boto
from boto.s3.key import Key

app = Flask(__name__)
# Enable/disable tagging. For debugging.
tagging = config.TAGGING_ENABLED

def chop(filename):
    '''
    The Screenshot "chop" View
    
    '''
    s3ThumbsURL = config.S3_THUMBS_URL
    s3FullURL = config.S3_FULL_URL
    s3MediumURL = config.S3_MEDIUM_URL
    
    chop = Post.objects.get(filename = filename)
    
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
    
    # For image linking, short url sharing.
    fullURL = config.DOMAIN_URL
    shortURL = config.SHORT_DOMAIN_URL
    
    # Calculate total score of post
    score = int(chop.upvotes) - int(chop.downvotes)
    
    return render_template('chops/chop.html', chop=chop, regForm=regForm,
                            loginForm=loginForm, fullURL=fullURL,
                            shortURL=shortURL, score=score, vote=vote, 
                            tagging=tagging, tagable=tagable, s3FullURL=s3FullURL,
                            s3MediumURL=s3MediumURL, s3ThumbsURL=s3ThumbsURL)
                            
@requires_auth        
def delete_chop(filename):
    ''' Controller to delete a chop post '''
    
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

