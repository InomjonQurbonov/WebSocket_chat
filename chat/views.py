from django.shortcuts import render, get_object_or_404, redirect
from chat.models import Room, Message, User
from rest_framework.permissions import IsAuthenticated
from chat.serializers import RoomSerializer, MessageSerializer
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from django.views.generic import ListView

class FirstPanel(ListView):
    model = Room
    template_name = 'first_panel.html'
    context_object_name = "rooms"

class RoomAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(request_body=RoomSerializer)
    def post(self, request):
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "data": serializer.data,
                "status": status.HTTP_201_CREATED,
                "success": True,
                "message": "Ma'lumot muvaffaqiyatli qo'shildi."
            }
            return Response(data=data)
        else:
            data = {
                "data": serializer.errors,
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "Ma'lumot yuborishda xatolik"
            }
            return Response(data=data)


class RoomDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, id):
        if Room.objects.filter(user1=request.user).filter(user2__id=id).exists():
            room = Room.objects.filter(user1=request.user).filter(user2__id=id).first()
            messages = Message.objects.filter(room=room)
            data = {
                "data": room.name,
                "messages":messages,
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Ma'lumot muvaffaqiyatli qo'shildi."
            }
            return Response(data=data)
        elif Room.objects.filter(user2=request.user).filter(user1__id=id).exists():
            room = Room.objects.filter(user2=request.user).filter(user1__id=id).first()
            messages = Message.objects.filter(room=room)
            data = {
                "data": room.name,
                "messages":messages,
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Ma'lumot muvaffaqiyatli qo'shildi."
            }
            return Response(data=data)
        else:
            user1 = request.user
            user2 = get_object_or_404(User, id=id)
            if user1.user_type==user2.user_type:
                room_name = f"{user1.username}{user2.username}"
                room = Room.objects.create(name=room_name)
                data = {
                    "data": room.name,
                    "messages":[],
                    "status": status.HTTP_200_OK,
                    "success": True,
                    "message": "Ma'lumot muvaffaqiyatli qo'shildi."
                }
                return Response(data=data)
            data = {
                "data": "Failed",
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "Ma'lumot almashish mumkin emas!"
            }
            return Response(data=data)


class MessageAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(request_body=MessageSerializer)
    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "data": serializer.data,
                "status": status.HTTP_201_CREATED,
                "success": True,
                "message": "Ma'lumot muvaffaqiyatli qo'shildi."
            }
            return Response(data=data)
        else:
            data = {
                "data": serializer.errors,
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "Ma'lumot yuborishda xatolik"
            }
            return Response(data=data)


def index(request):
    if not request.user.is_authenticated:
        return redirect("login-user")
    rooms = Room.objects.all()
    context = {
        'rooms':rooms
    }
    return render(request, 'home.html', context=context)


def room(request, room_name):
    if not request.user.is_authenticated:
        return redirect("login-user")
    if Room.objects.filter(name=room_name).exists():
        room = get_object_or_404(Room, name=room_name)
    else:
        room = Room.objects.create(name=room_name)
    messages = Message.objects.filter(room=room)
    return render(request, 'room.html', {'room_name': room_name, 'messages': messages})


def chatPage(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login-user")
    context = {}
    return render(request, "chatPage.html", context)