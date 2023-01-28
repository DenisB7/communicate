import json

from django.db.models import F
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from main.models import Profile, Messages


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.set_user_online()
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.set_user_offline()
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        await self.save_message_and_set_status(message)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))

    @database_sync_to_async
    def set_user_online(self):
        profile = Profile.objects.filter(user_id=self.scope["user"].pk)
        if profile.first().is_teacher:
            Messages.objects.filter(teacher_id=profile[0].pk).update(teacher_read=True)
            profile.update(teacher_online=1)
        elif profile.first().is_student:
            Messages.objects.filter(student_id=profile[0].pk).update(student_read=True)
            profile.update(student_online=1)

    @database_sync_to_async
    def set_user_offline(self):
        profile = Profile.objects.filter(user_id=self.scope["user"].pk)
        if profile.first().is_teacher:
            profile.update(teacher_online=0)
        elif profile.first().is_student:
            profile.update(student_online=0)

    @database_sync_to_async
    def save_message_and_set_status(self, message):
        profile = Profile.objects.get(user_id=self.scope["user"].pk)
        details = {'message': message}
        if profile.is_teacher:
            student = Profile.objects.get(is_student=True)
            details['student_id'] = student.pk
            details['teacher_id'] = profile.pk
            details['teacher_read'] = True
            if student.student_online == 0:
                details['student_read'] = False
            else:
                details['student_read'] = True
            Messages.objects.create(**details)
        elif profile.is_student:
            teacher = Profile.objects.get(is_teacher=True)
            details['student_id'] = profile.pk
            details['teacher_id'] = teacher.pk
            details['student_read'] = True
            if teacher.teacher_online == 0:
                details['teacher_read'] = False
            else:
                details['teacher_read'] = True
            Messages.objects.create(**details)
