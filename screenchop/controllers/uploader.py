#!/usr/bin/env python

'''
uploader.py - Controller to upload from form to s3, create thumbs and
store info in MongoDB.

'''
import os, sys
from time import strftime
import uuid

from flask import Flask
from flask import request, session
from flask import abort, redirect, url_for, jsonify
from flask import render_template, flash
from werkzeug import secure_filename

import boto
from boto.s3.key import Key

from PIL import Image

from screenchop import config
from screenchop.models import Post

app = Flask(__name__)

ALLOWED_EXTENSIONS = set(config.ALLOWED_FILE_TYPES)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def uploader():

    # Generate UUID.hex to use as filename
    uid = uuid.uuid4()
    generate_unique = uid.hex
    
    # Accept upload into object
    image = request.files['imageupload']
    uploadType = request.form['uploadType']
    
    if image and allowed_file(image.filename):
    
        # Create temp file
        image.save(config.TEMP_FILE_DIR + secure_filename(image.filename))

        
        # Set filename and file location securely
        filename = secure_filename(image.filename)
        
        # Build file locations for original and proxy images
        fullfile = config.TEMP_FILE_DIR + secure_filename(image.filename)
        medfile = config.TEMP_FILE_DIR + "medium." + secure_filename(image.filename)
        thumbfile = config.TEMP_FILE_DIR + "thumbnail." + secure_filename(image.filename)
        
        # Open image with PIL
        image = Image.open(fullfile)
        
        # For original width and height for Jglance
        width, height = image.size
        
        # Create 2 thumbs
        medsize = config.MEDIUM_MAX_WIDTH, config.MEDIUM_MAX_HEIGHT
        image.thumbnail(medsize, Image.ANTIALIAS)
        image.save(medfile, "JPEG")
        
        thumbsize = config.THUMB_MAX_WIDTH, config.THUMB_MAX_HEIGHT
        image.thumbnail(thumbsize, Image.ANTIALIAS)
        image.save(thumbfile, "JPEG")
        
        # Connect to S3 and set Key object.
        conn = boto.connect_s3(config.AWS_ACCESS_KEY_ID,
                                 config.AWS_SECRET_ACCESS_KEY)
                                 
        b = conn.get_bucket(config.BUCKET_NAME)

        k = Key(b)
        
        '''
        The following uploads the 3 sized images to S3
        
        '''
        # Set original file in bucket/full
        k.key = 'full/' + generate_unique
        
        # Upload file to S3 and make public URL
        k.set_contents_from_filename(fullfile)
        k.make_public
        k.set_acl('public-read')
        
        
        # Set medium file in bucket/med
        k.key = 'medium/' + generate_unique
        
        # Upload file to S3 and make public URL
        k.set_contents_from_filename(medfile)
        k.make_public
        k.set_acl('public-read')
        
        
        # Set thumb file in bucket/thumbs
        k.key = 'thumbs/' + generate_unique
        
        # Upload file to S3 and make public URL
        k.set_contents_from_filename(thumbfile)
        k.make_public
        k.set_acl('public-read')
        
        
        # Clean temp files
        os.remove(fullfile)
        os.remove(medfile)
        os.remove(thumbfile)
        
        # Create Post in MongoDB
        post = Post(title='test title',
                submitter=session['username'],
                caption='testing caption',
                tags= ['tera'], 
                comments=['asdfcomment'],
                thumbnail=generate_unique, 
                filename=generate_unique, 
                medium=generate_unique,
                date=strftime("%Y-%m-%d_%H-%M-%S"), 
                rating=4, 
                width=width, 
                height=height)

        post.save()

        if uploadType == 'single-upload':
            return redirect(url_for('upload'))
        else:
            return jsonify(result='success')
            
    else:
        flash("Invalid File - Please upload an image file. (png, jpg, jpeg)")
        return redirect(url_for('upload'))

