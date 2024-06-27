from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from chat.views import index, room, chatPage, RoomAPIView, MessageAPIView, RoomDetailAPIView


urlpatterns = [
    path("index/<str:room_name>/", chatPage, name="chat-page"),
    path('home/', index, name='index'),
    path('<str:room_name>/', room, name='room'),
    path("auth/login/", LoginView.as_view
         (template_name="LoginPage.html"), name="login-user"),
    path("auth/logout/", LogoutView.as_view(), name="logout-user"),
    path('room/', RoomAPIView.as_view()),
    path('room/<int:id>', RoomDetailAPIView.as_view()),
    path('message/', MessageAPIView.as_view()),
]