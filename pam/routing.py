from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from django.urls.conf import re_path
from user import consumers
from channels.security.websocket import AllowedHostsOriginValidator
from .middleware import TokenAuthMiddleware

websocket_urlpatterns = [
    #In routing.py, "as_asgi()" is required for versions over python 3.6.
    #path('user/command2/<str:username>', consumers.ChatConsumer.as_asgi()),
    re_path(r'user/command2/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()) # add ws for prefix.
]

application = ProtocolTypeRouter({
        'websocket': AllowedHostsOriginValidator(
            TokenAuthMiddleware(
                URLRouter(websocket_urlpatterns)
            )
        )
    })

