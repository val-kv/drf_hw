"""
WSGI config for DRF_HW project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import eventlet
from django.core.wsgi import get_wsgi_application


eventlet.monkey_patch()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DRF_HW.settings')

application = get_wsgi_application()
