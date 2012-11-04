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

