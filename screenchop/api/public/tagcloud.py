'''
tagcloud.py - JSON view to load tag cloud used by /tags view.

'''

from flask import jsonify

from screenchop.models import *
from screenchop import config

def tagcloud_json():
    ''' Tagcloud json view to generate tagcloud for /tags view. '''
    
    # Queries Tag_freq collection for all except null/None
    tags = Tag_freq.objects(tag__ne=None)
    
    #Query list of dictionaries for a JSON object. Construct a json response
    jsonTagsQuery = [
                        {
                           "tag": x.tag,
					       "freq": x.freq
                        } for x in tags
                    ]
    
    # Return json response
    return jsonify(tags=jsonTagsQuery)
