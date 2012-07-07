'''
tags.py - JSON view to load tags with given parameters and a save/delete
controller. Both controllers check if user session is logged in and is owner
of the post.

'''

from flask import Flask
from flask import request
from flask import abort, redirect, url_for, jsonify, session
from flask import render_template

from screenchop.models import *
from screenchop import config
from screenchop.sessions import requires_auth
import json, uuid

def getTags_json():
    '''
    Tags json view to display tag data from given parameters.
    
    '''
    
    # GET parameters for both Post UID and Filename
    postUID = request.args.get('postuid', '')
    postFilename = request.args.get('filename', '')
    
    # In case view called without parameters
    if postFilename == '':
        return 'Error: No postuid parameters given'
    
    # Load query Tag and Post to object matching filename
    tags = Tag.objects(postfilename=postFilename)
    try:
        post = Post.objects.get(filename=postFilename)
    except:
        return 'Post does not exist'
    
    # If session user is owner of tag, make editable
    if 'username' in session:
        if session['username'] == post.submitter:
            tagEditable = True
        else:
            tagEditable = False
    else:
        tagEditable = False

    
    #Query list of dictionaries for a JSON object. Construct a json response
    jsonTagsQuery = [
                        {  "top": x.top,
					       "left": x.left,
					       "width": x.width,
					       "height": x.height,
					       "text": x.text,
					       "id": x.uid,
					       "editable": tagEditable,
					       "postuid": x.postuid,
					       "filename": x.postfilename
                         } for x in tags]
    
    # Return json response
    return jsonify(tags=jsonTagsQuery)


@requires_auth
def saveTag():
    '''
    Controller when saving a tag. Checks if user owns the Post first.
    
    '''
    
    # GET request parameters
    getText = request.args.get('text')
    getHeight = request.args.get('height')
    getWidth = request.args.get('width')
    getTop = request.args.get('top')
    getLeft = request.args.get('left')
    getUID = request.args.get('id')
    getPostUID = request.args.get('postuid')
    getPostFilename = request.args.get('filename')
    
    # Generate unique id string for a new tag.
    tagUUID = str(uuid.uuid4())
    
    # Query Post with filename parameter and store submitter name
    post = Post.objects.get(filename=getPostFilename)
    submitter = post.submitter
    
    # Check if user is the submitter of the post
    if submitter == session['username']:
        pass
    else:
        return 'Error: Post does not belong to user.'
    
    # annotate.js will pass 'new' as an id parameter to a newly generated tag.
    # If the tag is new, we create a new tag. If it's not 'new', then atomically
    # update the post with new tag parameters.
    if getUID == 'new':
        # Create Tag in Mongo
        tag = Tag(
                uid=tagUUID,
                top=getTop,
                left=getLeft,
                width=getWidth,
                height=getHeight,
                text=getText,
                postuid=getPostUID,
                postfilename=getPostFilename,
                submitter=session['username']
                )
        tag.save()
    else:
        # Update
        Tag.objects(uid=getUID).update(set__top=getTop,
                                       set__left=getLeft,
                                       set__width=getWidth,
                                       set__height=getHeight,
                                       set__text=getText)

    
    # Returns json response. Though annotate doesn't really care unless exception.
    return jsonify(tags='saved tag')
    
@requires_auth
def deleteTag():
    '''
    Controller to delete a tag. Checks if session user is owner of post first.
    
    '''
    
    # GET parameters of tag id.
    getTagID = request.args.get('id')
    
    # Query Tag with id parameter
    tag = Tag.objects.get(uid=getTagID)
    
    # Check if submitter of tag is same as logged in user session
    if tag.submitter == session['username']:
        pass
    else:
        return 'Error: Post does not belong to user.'
    
    # Delete tag that matches tag id
    Tag.objects(uid=getTagID).delete()

    # Returns json response. Though annotate doesn't really care unless exception.
    return jsonify(tags='deleted tag')

