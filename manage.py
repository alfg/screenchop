#!/usr/bin/env python

from flaskext.script import Manager
from screenchop import urls

from scripts.add_invite_code import generate_invite
from scripts.tag_freq import tag_frequencies

manager = Manager(urls.app)

@manager.command
def invite_code():
    "Generates an invitation code"
    generate_invite()

@manager.command
def tag_freq():
    "Updates tag_freq collection with updated tag cloud"
    tag_frequencies()
    
    
if __name__ == '__main__':
    manager.run()
