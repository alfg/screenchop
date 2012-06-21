#!/usr/bin/env python

from flask import Flask
from flask import request, redirect, url_for, escape
from flask import render_template

from screenchop import config

#import views
from screenchop.views import home
from screenchop.controllers import upload
from screenchop.api import images
from screenchop.sessions import login, logout


app = Flask(__name__)
app.secret_key = config.SESSION_KEY

# All views below
app.add_url_rule('/', view_func=home.home)
app.add_url_rule('/uploads', view_func=home.uploads)

# Controllers
app.add_url_rule('/upload', view_func=upload.upload, methods=['POST'])

# APIs
app.add_url_rule('/api', view_func=images.getMainImages, methods=['GET'])

# Error Pages
@app.errorhandler(500)
def error_page(e):
    return render_template('error_pages/500.html'), 500

@app.errorhandler(404)
def not_found(e):
    return render_template('error_pages/404.html'), 404


# Sessions
app.add_url_rule('/login', view_func=login, methods=['POST', 'GET'])
app.add_url_rule('/logout', view_func=logout, methods=['POST', 'GET'])

