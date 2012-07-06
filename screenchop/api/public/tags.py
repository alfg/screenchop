from flask import Flask
from flask import request
from flask import abort, redirect, url_for, jsonify
from flask import render_template

from screenchop.models import *
from screenchop import config
import json, uuid

def getTags_json():
    
    postUID = request.args.get('postuid', '')
    postFilename = request.args.get('filename', '')
    
    if postFilename == '':
        return 'Error: No postuid parameters given'
    
    tags = Tag.objects(postfilename=postFilename)

    
    #Query list of dictionaries for a JSON object
    jsonTagsQuery = [
                        {  "top": x.top,
					       "left": x.left,
					       "width": x.width,
					       "height": x.height,
					       "text": x.text,
					       "id": x.uid,
					       "editable": True,
					       "postuid": x.postuid,
					       "filename": x.postfilename
                         } for x in tags]
    
    return jsonify(tags=jsonTagsQuery)
    
def saveTag():
    getText = request.args.get('text')
    getHeight = request.args.get('height')
    getWidth = request.args.get('width')
    getTop = request.args.get('top')
    getLeft = request.args.get('left')
    getUID = request.args.get('id')
    getPostUID = request.args.get('postuid')
    getPostFilename = request.args.get('filename')
    
    tagUUID = str(uuid.uuid4())
        
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
                postfilename=getPostFilename
                )
        tag.save()
    else:
        # Update
        Tag.objects(uid=getUID).update(set__top=getTop,
                                       set__left=getLeft,
                                       set__width=getWidth,
                                       set__height=getHeight,
                                       set__text=getText)

    

    return jsonify(tags='saved tag')
    
def deleteTag():
    getTagID = request.args.get('id')
    
    Tag.objects(uid=getTagID).delete()

    return jsonify(tags='deleted tag')

