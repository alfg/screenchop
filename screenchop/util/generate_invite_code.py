''' Code to run manually to generate invite codes. Run by manage.py'''

from mongoengine import *
import uuid
from screenchop.models import *


def generate_invite(username):
    # Generate UUID.hex to use as filename
    uid = uuid.uuid4()
    generate_unique = uid.hex

    code = Invite_code(code=generate_unique, created_by=username)
    code.save()

    return code.code

