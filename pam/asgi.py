"""
ASGI config for pam project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
from channels.security.websocket import AllowedHostsOriginValidator

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from pam.middleware import TokenAuthMiddleware
import pam.routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pam.settings')

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  'websocket': AllowedHostsOriginValidator(
            TokenAuthMiddleware(
                URLRouter(pam.routing.websocket_urlpatterns)
            )
        )
})
