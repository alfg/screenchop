#!/usr/bin/env python

from flask import Flask
from flask import request, redirect, url_for, escape
from flask import render_template

from screenchop import config

#import views
from screenchop.views import home, chops
from screenchop.controllers import uploader
from screenchop.api.public import images
from screenchop.sessions import login, logout, register


app = Flask(__name__)
app.secret_key = config.SESSION_KEY

# All views below
app.add_url_rule('/', view_func=home.home)
app.add_url_rule('/upload', view_func=home.upload)
app.add_url_rule('/account', view_func=home.account, methods=['POST', 'GET'])
app.add_url_rule('/<filename>', view_func=chops.chop, methods=['GET'])

# Controllers
app.add_url_rule('/uploader', view_func=uploader.uploader, methods=['POST'])
app.add_url_rule('/register', view_func=register, methods=['POST', 'GET'])

# APIs
app.add_url_rule('/api/public/images.json', view_func=images.getMainImages, methods=['GET'])

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
