from flask import Flask
from flask import request
from flask import abort, redirect, url_for, jsonify
from flask import render_template

from screenchop.models import *
from screenchop import config
import json

def getTags_json():
    
    tags = Tag.objects()
    
    #Query list of dictionaries for a JSON object
    jsonTagsQuery = [
                        {  "top": x.top,
					       "left": x.left,
					       "width": x.width,
					       "height": x.height,
					       "text": x.text,
					       "id": x.uid,
					       "editable": True
                         } for x in tags]
    
    return jsonify(tags=jsonTagsQuery)
    
def saveTag():
    getText = request.args.get('text')
    getHeight = request.args.get('height')
    getWidth = request.args.get('width')
    getTop = request.args.get('top')
    getLeft = request.args.get('left')
    getUID = request.args.get('id')
    
        
    if getUID == 'new':
        # Create Tag in Mongo
        tag = Tag(
                top=getTop,
                left=getLeft,
                width=getWidth,
                height=getHeight,
                text=getText,
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
    return jsonify(tags='delete tag')

