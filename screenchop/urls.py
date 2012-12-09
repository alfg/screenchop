#!/usr/bin/env python

from flask import Flask
from flask import request, redirect, url_for, escape
from flask import render_template
from flaskext.cache import Cache
from flask.ext.assets import Environment, Bundle

from screenchop import config

#import views
from screenchop.views import home, chops, account, user
from screenchop.controllers import uploader, vote, star, subscriptions, follow
from screenchop.api.public import images, tags, tagcloud, getuser
from screenchop.sessions import login, logout, register


app = Flask(__name__)
app.secret_key = config.SESSION_KEY
assets = Environment(app)
app.config['ASSETS_DEBUG'] = True 

js_libs = Bundle('js/lib/jquery.annotate.js',
                 'js/lib/jquery.filedrop.js', filters='jsmin', output='gen/js_libs.js')

js_custom = Bundle('js/custom/annotations.js',
                   'js/custom/dropscript.js',
                   'js/custom/login.js',
                   'js/custom/tooltips.js',
                   'js/custom/gallery.js',
                   'js/custom/votes.js',
                   'js/custom/tagcloud.js',
                   'js/custom/custom.js', filters='jsmin', output='gen/js_custom.js')

assets.register('js_libs', js_libs)
assets.register('js_custom', js_custom)


# All views below
app.add_url_rule('/', view_func=home.home)
app.add_url_rule('/top', view_func=home.home_top)
app.add_url_rule('/new', view_func=home.home_new)
app.add_url_rule('/tags/', view_func=home.tags)
app.add_url_rule('/tags/<tag>', view_func=home.tags_single)
app.add_url_rule('/upload', view_func=home.upload)
app.add_url_rule('/account', view_func=account.account, methods=['POST', 'GET'])
app.add_url_rule('/account/password', view_func=account.account_password, methods=['POST', 'GET'])
app.add_url_rule('/account/uploads', view_func=account.account_uploads, methods=['POST', 'GET'])
app.add_url_rule('/c/<filename>', view_func=chops.chop, methods=['GET'])
app.add_url_rule('/u/<username>', view_func=user.user, methods=['GET'])
app.add_url_rule('/following', view_func=home.following, methods=['GET'])
app.add_url_rule('/help/', view_func=home.help, methods=['GET'])
app.add_url_rule('/tos/', view_func=home.tos, methods=['GET'])
app.add_url_rule('/contact/', view_func=home.contact, methods=['GET', 'POST'])
app.add_url_rule('/request-invite/', view_func=home.request_invite, methods=['GET', 'POST'])

# Controllers
app.add_url_rule('/uploader', view_func=uploader.uploader, methods=['POST'])
app.add_url_rule('/urluploader', view_func=uploader.url_uploader, methods=['POST'])
app.add_url_rule('/register', view_func=register, methods=['POST', 'GET'])
app.add_url_rule('/upvote', view_func=vote.upvote, methods=['POST', 'GET'])
app.add_url_rule('/downvote', view_func=vote.downvote, methods=['POST', 'GET'])
app.add_url_rule('/tags/save', view_func=tags.saveTag, methods=['POST', 'GET'])
app.add_url_rule('/tags/delete', view_func=tags.deleteTag, methods=['POST', 'GET'])
app.add_url_rule('/account/avatar', view_func=account.account_avatar_uploader, methods=['POST'])
app.add_url_rule('/c/<filename>/delete', view_func=chops.delete_chop, methods=['POST', 'GET'])
app.add_url_rule('/c/<filename>/update', view_func=chops.update_chop, methods=['POST', 'GET'])
app.add_url_rule('/c/<filename>/report', view_func=chops.report_chop, methods=['POST', 'GET'])
app.add_url_rule('/star', view_func=star.star, methods=['POST', 'GET'])
app.add_url_rule('/tags/<tag>/subscribe', view_func=subscriptions.subscribe, methods=['POST', 'GET'])
app.add_url_rule('/tags/<tag>/unsubscribe', view_func=subscriptions.unsubscribe, methods=['POST', 'GET'])
app.add_url_rule('/u/<user>/follow', view_func=follow.follow, methods=['POST', 'GET'])
app.add_url_rule('/u/<user>/unfollow', view_func=follow.unfollow, methods=['POST', 'GET'])
app.add_url_rule('/account/generateInvite', view_func=account.account_generate_code, methods=['POST', 'GET'])

# APIs
app.add_url_rule('/api/public/images.json', view_func=images.getImages_view, methods=['GET'])
app.add_url_rule('/api/public/tags.json', view_func=tags.getTags_json, methods=['GET'])
app.add_url_rule('/api/public/tagcloud.json', view_func=tagcloud.tagcloud_json, methods=['GET'])
app.add_url_rule('/api/public/searchTags.json', view_func=tagcloud.searchTags_json, methods=['GET'])
app.add_url_rule('/api/public/following.json', view_func=getuser.userFollowing_json, methods=['GET'])

# Redirects to home
def redirect_to_home():
    return redirect('/') 

app.add_url_rule('/c/', view_func=redirect_to_home)

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

# Global Variables
@app.context_processor
def registration_level():
    return dict(registration_level=config.REGISTRATION_LEVEL)
    
@app.context_processor
def google_analytics_account():
    return dict(google_analytics_account=config.GOOGLE_ANALYTICS_ACCOUNT)

@app.context_processor
def debug_enabled():
    return dict(debug_enabled_account=config.DEBUG)
