#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import threading

import socket
import time
import threading
import datetime

import datetime
import os
# from First_App.utils import create_socket
# import pygame as pygame







def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'UIT_Roll_UP.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)






if __name__ == '__main__':
    main()




