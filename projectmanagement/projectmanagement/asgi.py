"""
ASGI config for projectmanagement project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from projectmanagement.telemetry import setup_telemetry


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectmanagement.settings')
setup_telemetry()
application = get_asgi_application()
