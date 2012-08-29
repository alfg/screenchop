from wtforms import Form, BooleanField, TextField, PasswordField
from wtforms import TextAreaField, FileField, validators
from flask.ext.wtf import url

from screenchop.util.custom_fields import TagListField 
from screenchop import config

class RegistrationForm(Form):
    username = TextField('Username', [
        validators.Length(min=3, max=20),
        validators.Required(message='Username must be between 3 and 20 characters long.')])
    password = PasswordField('New Password', [
        validators.Required(message='Password required'),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    if config.REGISTRATION_LEVEL == 'invite':
        invite_code = TextField('Invitation Code', [validators.Required(message='Invitation code required')])
    else:
        pass
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('Terms of Service', [validators.Required(message='You must agree to the Terms of Service')])

class LoginForm(Form):
    username = TextField('Username')
    password = PasswordField('Password')
    
class AccountForm(Form):
    newpass = PasswordField('New Password', [
        validators.Required(message='Password required'),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    currentpass = PasswordField('Current Password', [
        validators.Required(message='Current password required')
    ])

class ProfileForm(Form):
    description = TextAreaField('Profile Description', [
        validators.Length(max=300, message='Max 300 characters'),
        ])

class EditPost(Form):
    caption = TextAreaField('Caption', [
        validators.Length(max=100, message='Max 100 characters')
            ])
    tags = TagListField('Tags')

class AddFromURLForm(Form):
    caption = TextField()
    tags = TagListField()
    url = TextField(validators=[url()])

class SingleFileForm(Form):
    caption = TextField()
    tags = TagListField()
