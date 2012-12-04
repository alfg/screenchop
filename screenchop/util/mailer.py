import boto
from screenchop import config

conn = boto.connect_ses(
    aws_access_key_id = config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY)

def send_contact_email(name, email, comment):
    """ Mailer for Contact Post form and view. """

    template = """
                Name: %s \n
                Email: %s \n
                Comment/Question: %s \n
               """ % (name, email, comment)
    
    conn.send_email(
        config.ADMIN_EMAIL,
        'Contact Form Request from %s' % email,
        template,
        [config.ADMIN_EMAIL])

def send_request_invite_email(email):
    """ Mailer for Request Invite Post form and view. """

    template = """
                Email: %s \n
               """ % (email)
    
    conn.send_email(
        config.ADMIN_EMAIL,
        'Invite Code Request from %s' % email,
        template,
        [config.ADMIN_EMAIL])

def report_chop(chop):
    """ Mailer for reporting a post. """

    template = """
                Post reported: %sc/%s \n
               """ % (config.DOMAIN_URL, chop)
    
    conn.send_email(
        config.ADMIN_EMAIL,
        'Post reported - %sc/%s' % (config.DOMAIN_URL, chop),
        template,
        [config.ADMIN_EMAIL])
