from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def room(request, room_name):
    context = {
        "username": request.user.username,
        "user_is_authenticated": request.user.is_authenticated,
        "room_name": room_name,
    }
    return render(request, "chat/room.html", context)
