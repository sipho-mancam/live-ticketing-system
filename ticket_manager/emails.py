from django.core.mail import EmailMessage, BadHeaderError, send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import live_ticketing_system.settings as settings
from .tasks import send_html_email

import time

def send_html_email_async(subject, html_template, context, to_emails):
    return send_html_email.delay(subject, html_template, context, to_emails)


def start_mail_runner():

    while True:
        # go to the database, read the emails table
        # get the records to send emails to.
        # create email, from template, 
        # send the email, 
        # wait for the new run to go through.
        # clear the records after reading them, 
        # sleep for a minute, do the same thing again after.
        time.sleep(5)