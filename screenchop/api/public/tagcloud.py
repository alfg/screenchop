'''
tagcloud.py - JSON view to load tag cloud used by /tags view.

'''

from flask import jsonify

from screenchop.models import *
from screenchop import config

def tagcloud_json():
    ''' Tagcloud json view to generate tagcloud for /tags view. '''
    
    # Queries Tag_freq collection for all except null/None and ''
    tags = Tag_freq.objects(Q(tag__nin=['']) & Q(tag__exists=True))
    
    #Query list of dictionaries for a JSON object. Construct a json response
    jsonTagsQuery = [
                        {
                           "tag": x.tag,
					       "freq": x.freq
                        } for x in tags
                    ]
    
    # Return json response
    return jsonify(tags=jsonTagsQuery)
    
def searchTags_json():
    ''' Tagcloud json view to generate tagcloud for /tags view. '''
    
    # Queries Tag_freq collection for all except null/None and ''
    tags = Tag_freq.objects(Q(tag__nin=['']) & Q(tag__exists=True))
    
    #Query list of dictionaries for a JSON object. Construct a json response
    jsonTagsQuery = [x.tag for x in tags]
    
    # Return json response
    return jsonify(tags=jsonTagsQuery)
