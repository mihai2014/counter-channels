from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
import asyncio
import json

STATE = 0
USERS = 0

class counter(AsyncWebsocketConsumer):
    
    async def connect(self):
        global STATE, USERS

        USERS = USERS + 1
        print("users:", USERS)

        self.group_name = "counter-strike"

        # Join room group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Send message to group: update users
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'group_message',
                'key1': 'type',
                'val1': 'users',
                'key2': 'count',
                'val2': USERS, 
            },                     
        )

        #prevent timing out of sending data 
        await asyncio.sleep(0.5)
        
        # Send message to group: update counter
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'group_message',
                'key1': 'type',
                'val1': 'state',
                'key2': 'value',
                'val2': STATE, 
            }
        )

        print("ready")

    async def disconnect(self, close_code):
        global STATE, USERS

        USERS = USERS - 1
        print("users:", USERS)

        # Send message to group: update users
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'group_message',
                'key1': 'type',
                'val1': 'users',
                'key2': 'count',
                'val2': USERS, 
            }
        )

        # Leave room group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        global STATE, USERS

        data = json.loads(text_data)
        if data["action"] == "minus":
            STATE -= 1
           
        elif data["action"] == "plus":
            STATE += 1
           
        print(data)

        # Send message to group: update counter
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'group_message',
                'key1': 'type',
                'val1': 'state',
                'key2': 'value',
                'val2': STATE, 
            }
        )

  
    async def group_message(self, event):
        key1 = event['key1']
        val1 = event['val1']
        key2 = event['key2']
        val2 = event['val2']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            key1 : val1, key2 : val2
        }))        