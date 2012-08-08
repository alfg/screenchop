#!/usr/bin/env python

''' tag_freq.py - Queries a list of frequently used tags from posts/chops.
This will then update the tag_freq Mongo collection with data for less resource
heavy querying on the /tags view. '''

from mongoengine import *
from screenchop.models import Post, Tag_freq

from operator import itemgetter

def tag_frequencies():
    ''' Finds frequently used tags in Posts and sorts them into tuples. '''
    
    tag_freqs = Post.objects.item_frequencies('tags', normalize=False)
    top_tags = sorted(tag_freqs.items(), key=itemgetter(1), reverse=True)[:10]
    
    # Print output and save results into Tag_freq collection
    for tag, freq in top_tags:
        print tag, int(freq)
        a, created = Tag_freq.objects.get_or_create(tag=tag)
        Tag_freq.objects(tag=tag).update_one(set__freq=int(freq))


