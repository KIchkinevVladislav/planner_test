import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planner.settings')

# Get the ASGI application for regular HTTP requests
asgi_application = get_asgi_application()

# Configure the ProtocolTypeRouter to handle WebSocket connections
application = ProtocolTypeRouter({
	'http': asgi_application,
	'websocket':
	AllowedHostsOriginValidator(
		AuthMiddlewareStack(
			URLRouter(chat.routing.websocket_urlpatterns)
		),
	)
})