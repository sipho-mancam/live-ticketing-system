#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import signal
from ticket_manager.emails import mail_execution_thread as execution_thread
import threading

def on_server_shutdown(signal, frame, stop_thread:threading.Thread=None):
    print("Waiting for the mailing service to finish ...")
    execution_thread.stop()
    execution_thread.join()
    print("Mailing service finished ...")
    sys.exit(0)

# Register the signal handler for server shutdown
signal.signal(signal.SIGTERM, on_server_shutdown)
signal.signal(signal.SIGINT, on_server_shutdown)


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'live_ticketing_system.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    execution_thread.start()
    try:
        execute_from_command_line(sys.argv)
    except KeyboardInterrupt as ki:
        on_server_shutdown(signal.SIGINT, None)

if __name__ == '__main__':
    main()
