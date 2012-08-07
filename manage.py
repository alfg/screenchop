#!/usr/bin/env python

from flaskext.script import Manager
from screenchop import urls

from scripts.add_invite_code import generate_invite

manager = Manager(urls.app)

@manager.command
def invite_code(help='Generates an invitation code'):
    "Generates an invitation code"
    generate_invite()
    
    
if __name__ == '__main__':
    manager.run()
