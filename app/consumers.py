from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer

import json
import asyncio
import logging

logging.basicConfig()

STATE = {"value": 0}
USERS = 0


class counter(AsyncWebsocketConsumer):

    async def connect(self):
        global USERS
        USERS = USERS + 1
        print("users:", USERS)

        #self.room_name = self.scope['url_route']['kwargs']['room_name']
        #self.room_group_name = 'chat_%s' % self.room_name

        self.room_name = "counter"
        self.room_group_name = "counter-strike"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Send message to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'update_users',
                #'message': message
            }
        )

        # Send message to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'update_counter',
                #'message': message
            }
        )

    async def disconnect(self, close_code):
        global USERS
        USERS = USERS - 1
        print("users:", USERS)

        # Send message to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'update_users',
                #'message': message
            }
        )

        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):

        data = json.loads(text_data)
        if data["action"] == "minus":
            STATE["value"] -= 1
            #await notify_state()
        elif data["action"] == "plus":
            STATE["value"] += 1
            #await notify_state()  

        print(data)

        # Send message to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'update_counter',
                #'message': message
            }
        )



    # Send message to group
    async def update_counter(self, event):
        global STATE
        #message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "type": "state", **STATE
        }))

    async def update_users(self, event):
        global USERS

        await self.send(text_data=json.dumps({
            "type": "users", "count": USERS
        }))    