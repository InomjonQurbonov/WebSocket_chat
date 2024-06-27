from django.urls import re_path
from django.urls import path
from chat.consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r'chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
]




# from django.urls import path , include
# from chat.consumers import ChatConsumer

# # Here, "" is routing to the URL ChatConsumer which 
# # will handle the chat functionality.
# websocket_urlpatterns = [
#     path("" , ChatConsumer.as_asgi()) , 
# ] 