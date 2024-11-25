"""
ASGI config for facemap project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from reconvisual.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'facemap.settings')

# Configuração do ProtocolTypeRouter para suportar WebSockets e HTTP
application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Suporte para requisições HTTP padrão
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns  # Roteamento de URLs para WebSockets
        )
    ),
})