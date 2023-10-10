from celery import shared_task
from django.core.mail import EmailMessage, BadHeaderError, send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import live_ticketing_system.settings as settings
import pathlib

@shared_task
def send_html_email(subject, html_template, context, to_emails):
    # Load the HTML template and generate the text content
    html_content = render_to_string(html_template, context)
    text_content = strip_tags(html_content)  # Remove HTML tags for the plain text part

    # Create the email message
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=to_emails
    )
    email.attach_alternative(html_content, "text/html")
    # Send the email
    email.send()

