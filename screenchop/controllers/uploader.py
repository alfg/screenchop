#!/usr/bin/env python

'''
uploader.py - Controller to upload from form to s3, create thumbs and
store info in MongoDB. Needs much refactoring and optimizing.

'''
import os, sys
from time import strftime
import uuid
import requests

from flask import Flask
from flask import request, session
from flask import abort, redirect, url_for, jsonify
from flask import render_template, flash, Markup
from werkzeug import secure_filename

import boto
from boto.s3.key import Key

from PIL import Image

from screenchop import config
from screenchop.sessions import requires_auth
from screenchop.models import Post
from screenchop.util import short_url, uploader_utils
from screenchop.forms import AddFromURLForm, SingleFileForm 

ALLOWED_EXTENSIONS = set(config.ALLOWED_FILE_TYPES)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@requires_auth
def uploader():
    """
    This is the upload controller used when uploading by single file or bulk
    drag and drop uploading.
    
    TODO: Optimize and create class with methods for each process.
    
    """

    # Accept Form for caption and tags
    singleFileForm = SingleFileForm(request.form)
    
    # Accept upload into object
    image = request.files['imageupload']
    uploadType = request.form['uploadType']
    
    # If single file upload, then store some extra request.form values
    if uploadType == 'single-upload':

        # Store optional fields into variables if they exist
        caption = singleFileForm.caption.data 
        tags = singleFileForm.tags.data

    # Otherwise, just set them to None as there's no data.
    else:
        caption, tags = None, None 
    
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
        
        
        
        
        # Create Post in MongoDB
        post = Post(submitter=session['username'],
                caption=caption,
                tags=tags, 
                width=width, 
                height=height)
        
        uploader_utils.set_upvote(post.submitter, post.uid)
        post.save()
        
        # set url as a short url to store as filename to S3 and Post Document
        url = short_url.encode_url(post.uid)
        
        ###
        ### The following uploads the 3 sized images to S3
        ###
        
        # Connect to S3 and set Key object.
        conn = boto.connect_s3(config.AWS_ACCESS_KEY_ID,
                                 config.AWS_SECRET_ACCESS_KEY)
                                 
        b = conn.get_bucket(config.BUCKET_NAME)
        k = Key(b)
        
        
        # Set original file in bucket/full
        k.key = 'full/' + url
        
        # Upload file to S3 and make public URL
        k.set_contents_from_filename(fullfile)
        k.make_public
        k.set_acl('public-read')
        
        
        # Set medium file in bucket/med
        k.key = 'medium/' + url
        
        # Upload file to S3 and make public URL
        k.set_contents_from_filename(medfile)
        k.make_public
        k.set_acl('public-read')
        
        
        # Set thumb file in bucket/thumbs
        k.key = 'thumbs/' + url
        
        # Upload file to S3 and make public URL
        k.set_contents_from_filename(thumbfile)
        k.make_public
        k.set_acl('public-read')
        
        
        # Clean temp files
        os.remove(fullfile)
        os.remove(medfile)
        os.remove(thumbfile)
        
        # Atomically update Post document to Store url
        Post.objects(id=post.id).update_one(set__filename=url)


        if uploadType == 'single-upload':
            flash(Markup('Screenshot uploaded - <a href="%sc/%s">View here</a>.' % (config.DOMAIN_URL, url)), 'uploaded')
            return redirect(url_for('upload'))
        else:
            return jsonify(result='success', url=('%sc/%s' % (config.DOMAIN_URL, url)))
            
    else:
        flash("Invalid File - Please upload an image file. (png, jpg, jpeg)")
        return redirect(url_for('upload'))



@requires_auth
def url_uploader():
    """
    This is the upload controller used when uploading by URL.
    
    TODO: Optimize and create class with methods for each process. Merge with 
    uploader() code.
    
    """
    urlForm = AddFromURLForm(request.form)
    
    imageurl = urlForm.url.data 
    
    try:
        r = requests.get(imageurl)
        image = r.content
        imagefilename = (r.url).split('/')[-1]
        
    except:
        flash("Invalid File - Please upload an image file. (png, jpg, jpeg)")
        return redirect(url_for('upload'))


    # Store optional fields into variables if they exist
    tags = urlForm.tags.data
    caption = urlForm.caption.data
    
    if image and allowed_file(imagefilename):
        try:
            # Create temp file
            with open(config.TEMP_FILE_DIR + secure_filename(imagefilename), "wb") as tmp:
                tmp.write(r.content)
            
            # Set filename and file location securely
            filename = secure_filename(imagefilename)
            
            # Build file locations for original and proxy images
            fullfile = config.TEMP_FILE_DIR + secure_filename(imagefilename)
            medfile = config.TEMP_FILE_DIR + "medium." + secure_filename(imagefilename)
            thumbfile = config.TEMP_FILE_DIR + "thumbnail." + secure_filename(imagefilename)
            
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
            
            
            
            
            # Create Post in MongoDB
            post = Post(submitter=session['username'],
                    caption=caption,
                    tags=tags, 
                    width=width, 
                    height=height)

            uploader_utils.set_upvote(post.submitter, post.uid)
            post.save()
            
            # set url as a short url to store as filename to S3 and Post Document
            url = short_url.encode_url(post.uid)
            
            ###
            ### The following uploads the 3 sized images to S3
            ###
                    
            # Connect to S3 and set Key object.
            conn = boto.connect_s3(config.AWS_ACCESS_KEY_ID,
                                     config.AWS_SECRET_ACCESS_KEY)
                                     
            b = conn.get_bucket(config.BUCKET_NAME)
            k = Key(b)
            
            
            # Set original file in bucket/full
            k.key = 'full/' + url
            
            # Upload file to S3 and make public URL
            k.set_contents_from_filename(fullfile)
            k.make_public
            k.set_acl('public-read')
            
            
            # Set medium file in bucket/med
            k.key = 'medium/' + url
            
            # Upload file to S3 and make public URL
            k.set_contents_from_filename(medfile)
            k.make_public
            k.set_acl('public-read')
            
            
            # Set thumb file in bucket/thumbs
            k.key = 'thumbs/' + url
            
            # Upload file to S3 and make public URL
            k.set_contents_from_filename(thumbfile)
            k.make_public
            k.set_acl('public-read')
            
            
            # Clean temp files
            os.remove(fullfile)
            os.remove(medfile)
            os.remove(thumbfile)
            
            # Atomically update Post document to Store url
            Post.objects(id=post.id).update_one(set__filename=url)

            flash(Markup('Screenshot uploaded - <a href="%sc/%s">View here</a>.' % (config.DOMAIN_URL, url)), 'uploaded')
            return redirect(url_for('upload'))
        except:
        
            # Clean temp files
            if os.path.isfile(fullfile):
                os.remove(fullfile)
            if os.path.isfile(medfile):
                os.remove(medfile)
            if os.path.isfile(thumbfile):
                os.remove(thumbfile)
            
            flash("Invalid File - Please upload an image file. (png, jpg, jpeg)")
            return redirect(url_for('upload'))
        
        
    else:
        flash("Invalid File - Please upload an image file. (png, jpg, jpeg)")
        return redirect(url_for('upload'))
