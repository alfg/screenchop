#!/usr/bin/env python

from flask import Flask
from flask import request, session, redirect, url_for
from flask import render_template, flash

from screenchop.models import *
from screenchop import config
from screenchop.forms import RegistrationForm, LoginForm, AccountForm, ProfileForm

from screenchop.sessions import *

app = Flask(__name__)

@requires_auth
def account():
    '''
    The Account View
    
    '''
    
    user = User.objects.get(username=session['username'])
    chops = Post.objects(submitter=session['username'])
    form = ProfileForm(request.form, description=user.description)
    
    # Calculate total score by adding all upvotes subtracted by all downvotes
    upvotes = 0
    downvotes = 0
    
    for n in chops:
        upvotes = upvotes + n.upvotes
        downvotes = downvotes + n.downvotes
    score = upvotes - downvotes
    
    
    if request.method == 'POST' and form.validate():
        user.description = form.description.data
        user.save()
        flash('Account updated')
        return redirect(url_for('account'))
    else:
    
        return render_template('main/account.html', user=user, score=score, form=form)

@requires_auth
def account_password():
    '''
    The Account Password View
    
    '''
    user = User.objects.get(username = session['username'])
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

