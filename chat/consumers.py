from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model

from .models import Group, Message
import json

User = get_user_model()


class JoinAndLeave(WebsocketConsumer):
	def connect(self):
		# Get the unique identifier for the chat room from the URL parameters
		self.room_uuid = self.scope['url_route']['kwargs']['uuid']
		# Create a unique group name for this chat room
		self.room_group_name = f'chat_{self.room_uuid}'

		# Add the channel (connection) to the group
		async_to_sync(self.channel_layer.group_add)(
		    self.room_group_name, self.channel_name
		)
		# Accept the WebSocket connection
		self.accept()


	def receive(self, text_data):
		# Receive a message from the WebSocket
		text_data_json = json.loads(text_data)
		message = text_data_json['message']
		user_id = self.scope['user'].id

		# Get the user and group based on the received data
		user = User.objects.get(id=user_id)
		group = Group.objects.get(uuid=self.room_uuid)

		# Save the received message to the database
		db_insert = Message(author=user,content=message,group=group)
		db_insert.save()

		# Broadcast the message to the group
		async_to_sync(self.channel_layer.group_send)(
		    self.room_group_name, {'type': 'chat_message', 'message': f'{user.get_full_name()}: {message}'}
		)

	def disconnect(self, close_code):
		# Remove the channel (connection) from the group when disconnected
		async_to_sync(self.channel_layer.group_discard)(
		    self.room_group_name, self.channel_name
		)

	def chat_message(self, event):
		# Receive the broadcasted message from the group
		message = event['message']
		# Send the message to the WebSocket
		self.send(text_data=json.dumps({'message': message}))