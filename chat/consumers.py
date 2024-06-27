import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_name = "doston"
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        message = text_data_json['message']
        sender = text_data_json["sender"]

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        sender = event["sender"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))


# adashmasam yo'' anuq xato buuuuuuuuuuuu🥹🥹🥹

# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from asgiref.sync import async_to_sync

# class ChatConsumer(AsyncWebsocketConsumer):

#     async def connect(self):
#         self.roomGroupName = "group_chat_gfg"
#         await self.channel_layer.group_add(
#             self.roomGroupName,
#             self.channel_name
#         )
#         await self.accept()

#     async def disconnect(self , close_code):
#         await self.channel_layer.group_discard(
#             self.roomGroupName,
#             self.channel_layer 
#         )
    
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json["message"]
#         username = text_data_json["sender"]
#         await self.channel_layer.group_send(
#             self.roomGroupName,{
#                 "type" : "sendMessage" ,
#                 "message" : message , 
#                 "username" : username ,
#         })

#     async def sendMessage(self , event) : 
#         message = event["message"]
#         username = event["username"]
#         await self.send(text_data = json.dumps({"message":message ,"username":username}))