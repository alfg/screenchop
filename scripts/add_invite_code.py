#!/usr/bin/env python

''' Script to run manually to generate invite codes. Run by manage.py'''

from mongoengine import *
import uuid
from screenchop.models import *


def generate_invite():
    # Generate UUID.hex to use as filename
    uid = uuid.uuid4()
    generate_unique = uid.hex

    code = Invite_code(code=generate_unique)

    code.save()
    
    print 'Invite code: %s' % generate_unique

