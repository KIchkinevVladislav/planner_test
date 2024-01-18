from django.urls import path
from . import consumers

# Define WebSocket URL patterns, associating the WebSocket consumer
# 'JoinAndLeave' with the path 'ws/open_chat/<uuid>/'. This allows
# WebSocket connections to be established for opening and participating
# in a chat room identified by the unique 'uuid'.
websocket_urlpatterns = [
	path(r"ws/open_chat/<uuid>/", consumers.JoinAndLeave.as_asgi())
]