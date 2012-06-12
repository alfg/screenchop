#!/usr/bin/env python

from flask import Flask
from flask import request
from flask import render_template

from screenchop import config

#import views
from screenchop.views import home
from screenchop.controllers import upload

app = Flask(__name__)


# All views below
app.add_url_rule('/', view_func=home.home)
app.add_url_rule('/uploads', view_func=home.uploads)

# Controllers
app.add_url_rule('/upload', view_func=upload.upload, methods=['POST'])

# Error Pages
@app.errorhandler(500)
def error_page(e):
    return render_template('error_pages/500.html'), 500

@app.errorhandler(404)
def not_found(e):
    return render_template('error_pages/404.html'), 404

