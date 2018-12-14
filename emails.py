from flask import request, session, url_for
from flask_mail import Mail, Message
import traceback
from main.models.user import Emails

__author__ = 'hughson.simon@gmail.com'

mail = Mail()

unsubscribe_message = '\n\nTo unsubscribe from these alerts, reply with UNSUBSCRIBE in the subject line.'

def send_email(
        subject,
        recipients,
        message,
        cc=[],
        bcc=[],
        attachment_filename=None,
        attachment_content_type='application/octet-stream',
        attachment_data=None):
    if not recipients and cc:
        recipients = cc
        cc = []
    msg = Message( body=message, subject=subject, recipients=recipients, cc=cc, bcc=bcc + ['hughson.simon@gmail.com'])
    if attachment_data:
        msg.attach(attachment_filename, attachment_content_type, attachment_data)
    mail.send(msg)

def error_email(code=""):
    message = ('URL: %s' % request.path) + '\n\n'
    message += ''.join(traceback.format_exc())
    send_email('Rateit Server Error' + code, ['hughson.simon@gmail.com'], message)

def user_register_email(user, hashes):

    link = "http://localhost:5001/api/activate_account?hashes="+str(hashes)
    email_records = Emails.query.filter_by(email_slug="register").first()
    print(email_records.email_subject)
    message = email_records.email_message
    message = message.replace("<-FIRSTNAME->", user.first_name)
    #message = message.replace("<-LASTNAME->", user.last_name)
    message = message.replace("<-ACTIVATIONLINK->", link)
    send_email(email_records.email_subject, [user.email], message)