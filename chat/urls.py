from django.urls import path

from chat.views import room

urlpatterns = [
    path("chat/<str:room_name>", room, name="room"),
]
