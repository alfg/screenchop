#!/usr/bin/env python

from flask import Flask
from flask import request, session, redirect, url_for
from flask import render_template, flash
from werkzeug import secure_filename

from screenchop.models import *
from screenchop import config
from screenchop.forms import RegistrationForm, LoginForm, AccountForm, ProfileForm
from screenchop.util.allowed_images import *
from screenchop.util.generate_invite_code import *

from screenchop.sessions import *

import boto
from boto.s3.key import Key

from PIL import Image, ImageOps

import os
import uuid

app = Flask(__name__)

@requires_auth
def account():
    '''
    The Account View
    
    '''
    
    user = User.objects.get(username=session['username'])
    chops = Post.objects(submitter=session['username'])
    form = ProfileForm(request.form, description=user.description)
    codes = Invite_code.objects(created_by=session['username'])
    for code in codes:
        print code.code
    
    avatarURL = config.S3_AVATAR_URL
    
    # Calculate total score by adding all upvotes subtracted by all downvotes
    upvotes = 0
    downvotes = 0
    
    for n in chops:
        upvotes = upvotes + n.upvotes
        downvotes = downvotes + n.downvotes
    score = upvotes - downvotes

    # Count number of followers and following
    followerCount = len(User.objects(following__in=[user.username]))
    followingCount = len(user.following)
    
    
    if request.method == 'POST' and form.validate():
        user.description = form.description.data
        user.save()
        
        flash('Account updated')
        return redirect(url_for('account'))
    else:
    
        return render_template('main/account.html', user=user, score=score,
                                                    form=form, avatarURL = avatarURL,
                                                    followerCount=followerCount,
                                                    followingCount=followingCount,
                                                    codes=codes)

@requires_auth
def account_password():
    '''
    The Account Password View
    
    '''
    user = User.objects.get(username=session['username'])
    form = AccountForm(request.form)
    if request.method == 'POST' and form.validate():
        if check_password_hash(user.password, form.currentpass.data):
            User.objects(username=session['username']).update(set__password=generate_password_hash(form.newpass.data))
            flash('Account updated')
            return redirect(url_for('account_password'))
        else:
            flash('Current password did not match. Account not updated')
            return redirect(url_for('account_password'))
        
    return render_template('main/account_password.html', user=user, form=form)
    
@requires_auth
def account_uploads():
    '''
    The account/uploads view.
    Displays any uploaders by user logged in.
    '''
    
    s3ThumbsURL = config.S3_THUMBS_URL
    chops = Post.objects(submitter=session['username'])

    return render_template('main/account_uploads.html',
                            s3ThumbsURL=s3ThumbsURL, chops=chops)
        

                               
@requires_auth
def account_avatar_uploader():
    '''
    Upload controller for avatar uploads.
    
    '''
    
    image = request.files['avatar']
    
    # Generate UUID.hex to use as filename
    uid = uuid.uuid4()
    generate_unique = uid.hex
    
    if image and allowed_file(image.filename):
    
        # Create temp file
        image.save(config.TEMP_FILE_DIR + secure_filename(image.filename))
        
        # Set filename and file location securely
        filename = secure_filename(image.filename)
        
        # Build file locations for original and proxy images
        fileloc = config.TEMP_FILE_DIR + secure_filename(image.filename)
        
        # Using PIL, create thumbnail for avatar and size it to fit 75x75
        size = (75, 75)
        image = Image.open(fileloc)
        thumb = ImageOps.fit(image, size, Image.ANTIALIAS)
        thumb.save(fileloc, "JPEG")
         
        # Connect to S3 and set Key object.
        conn = boto.connect_s3(config.AWS_ACCESS_KEY_ID,
                                 config.AWS_SECRET_ACCESS_KEY)
                                 
        b = conn.get_bucket(config.BUCKET_NAME)
        k = Key(b)
        
        
        # Set original file in bucket/full
        k.key = 'avatar/' + generate_unique
        
        # Upload file to S3 and make public URL
        k.set_contents_from_filename(fileloc)
        k.make_public
        k.set_acl('public-read')
        
        
        # Clean temp files
        os.remove(fileloc)
        
        # Atomically update Account document to Store avatar key
        User.objects(username=session['username']).update_one(set__avatar=generate_unique)
        
    else:
        flash('Only JPG, JPEG, and PNG images allowed')
        return redirect(url_for('account'))
    
    flash('Avatar Updated')
    return redirect(url_for('account'))
    
@requires_auth
def account_generate_code():
    """ Generate Invite Code Controller """
    
    
    user = User.objects.get(username=session['username'])
    valid_codes = len(Invite_code.objects(created_by=session['username'], valid=True))

    if request.method == 'POST' and valid_codes < 5:
        generate_invite(user.username)
        
        flash('Code generated')
        return redirect(url_for('account'))
    else:
    
        flash('You may only have up to 5 valid invite codes at a time.')
        return redirect(url_for('account'))

