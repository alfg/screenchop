'''
tagcloud.py - JSON view to load tag cloud used by /tags view.

'''

from flask import Flask
from flask import request
from flask import abort, redirect, url_for, jsonify, session
from flask import render_template

from screenchop.models import *
from screenchop import config
from screenchop.sessions import requires_auth
import json, uuid

def tagcloud_json():
    '''
    Tagcloud json view to generate tagcloud for /tags view.
    
    '''

    #Query list of dictionaries for a JSON object. Construct a json response
    jsonTagsQuery = [
                        {  "tag": "#test",
                           "freq": "1"
                         },
                         
                         {  "tag": "#test2",
                           "freq": "2"
                         },
                         
                         {  "tag": "#test3",
                           "freq": "3"
                         },
                         
                         {  "tag": "#test",
                           "freq": "1"
                         },
                         
                         {  "tag": "#test2",
                           "freq": "2"
                         }
                     
                     ]
    '''
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
    '''
    
    # Return json response
    return jsonify(tags=jsonTagsQuery)
