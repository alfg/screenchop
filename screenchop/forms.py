from wtforms import Form, BooleanField, TextField, PasswordField
from wtforms import TextAreaField, FileField, validators

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
    accept_tos = BooleanField('I agree to the Terms of Service', [validators.Required(message='You must agree to the Terms of Service')])

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
    description = TextAreaField('Profile Description')
