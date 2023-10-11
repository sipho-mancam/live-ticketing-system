from django.core.mail import EmailMessage, BadHeaderError, send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import live_ticketing_system.settings as settings
from .tasks import send_html_email
import threading
from lt_db_ops import db_connector, utils, parse2JSON, constants
import time

def send_html_email_async(subject, html_template, context, to_emails):
    return send_html_email.delay(subject, html_template, context, to_emails)

class MailExecutionThread(threading.Thread):
    def __init__(self)->None:
        super().__init__()
        self._stop_event = threading.Event()
    
    def run(self):
        while not self._stop_event.is_set():
            self.start_mail_runner()
        
    def start_mail_runner(self):
        # go to the database, read the emails table
        # get the records to send emails to.
        # create email, from template, 
        # send the email, 
        # wait for the new run to go through.
        # clear the records after reading them, 
        # sleep for a minute, do the same thing again after.
        template = constants.TEMPLATE_BASE_PATH
        connector = db_connector.create_db_connector()
        unsent_mail = connector.get_unsent_records()
        sent_list = []
        for mail in unsent_mail:
            temporary_template = template + mail[constants.COL_ER_TEMPLATE]
            to_email = [f"{mail['recipient_email']}"]
            context = {}
            context['recipient_name'] = mail['recipient_name']
            context['actuator'] = mail['actuator']
            context['ticket_id'] = mail['ticket_id']
            context['timestamp'] = mail['time_stamp']
            subject = "[" + mail['subject'] + "]" + " Ticket ID #"+str(mail['ticket_id'])

            send_html_email(subject, temporary_template, context, to_email)

            sent_list.append(mail[constants.COL_ER_ID])
        connector.update_unsent_to_sent_batch(sent_list)
        connector.close_connection()
        time.sleep(3)

    def stop(self):
        self._stop_event.set()
    

mail_execution_thread = MailExecutionThread()

