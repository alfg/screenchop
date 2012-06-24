#!/usr/bin/env python

'''
Upload.py - Controller to upload from form to s3 and store info in MongoDB

'''
import os
from time import strftime

from flask import Flask
from flask import request, session
from flask import abort, redirect, url_for, jsonify
from flask import render_template
from werkzeug import secure_filename

import boto
from boto.s3.key import Key

from PIL import Image

from screenchop import config
from screenchop.models import Post

app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def upload():
    # Accept upload into object
    image = request.files['imageupload']
    uploadType = request.form['uploadType']
    
    if image and allowed_file(image.filename):
    
        # Create temp file
        image.save(config.TEMP_FILE_DIR + secure_filename(image.filename))
        
        # Set filename and file location securely
        filename = secure_filename(image.filename)
        fileloc = config.TEMP_FILE_DIR + secure_filename(image.filename)
        
        # Setting metadata from image using PIL
        imageMeta = Image.open(fileloc)
        width, height = imageMeta.size
        
        # Connect to S3
        conn = boto.connect_s3(config.AWS_ACCESS_KEY_ID,
                                 config.AWS_SECRET_ACCESS_KEY)
                                 
        b = conn.get_bucket(config.BUCKET_NAME)

        k = Key(b)

        # Set Key from filename
        k.key = 'thumbs/' + filename
        
        # Upload file to S3 and make public URL
        k.set_contents_from_filename(fileloc)
        k.make_public
        k.set_acl('public-read')
        
        # Clean temp file
        os.remove(fileloc)
        
        # Create Post in MongoDB
        post = Post(title='test title',
                submitter=session['username'],
                caption='testing caption',
                tags= ['tera'], 
                comments=['asdfcomment'],
                thumbnail=filename, 
                filename=filename, 
                date=strftime("%Y-%m-%d_%H-%M-%S"), 
                rating=4, 
                width=width, 
                height=height)

        post.save()

        if uploadType == 'single-upload':
            return redirect(url_for('uploads'))
        else:
            return jsonify(result='success')
            
    else:
        error = "Invalid File"
        return render_template("main/uploads.html", error=error)

