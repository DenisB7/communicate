import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from main.models import Messages


@login_required
def room(request, room_name):
    old_messages = Messages.objects.all()
    if old_messages:
        old_messages = '\n'.join(message.message for message in old_messages)
    context = {
        "username": request.user.username,
        "user_is_authenticated": request.user.is_authenticated,
        "room_name": room_name,
        "old_messages": old_messages,
    }
    return render(request, "chat/room.html", context)
