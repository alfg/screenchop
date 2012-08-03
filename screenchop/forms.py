from wtforms import Form, BooleanField, TextField, PasswordField, TextAreaField, validators

class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('New Password', [
        validators.Required(message='Password required'),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.Required(message='Accept ToS')])

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
