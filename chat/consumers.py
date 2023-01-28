import json

from django.db.models import F
from channels.generic.websocket import AsyncWebsocketConsumer
from main.models import Profile, Messages


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        profile = Profile.objects.get(user_id=self.scope["user"].pk)
        if profile.is_teacher:
            Messages.objects.filter(teacher_id=profile.pk).update(teacher_read=True)
            profile.update(teacher_online=F("teacher_online") + 1)
        elif profile.is_student:
            Messages.objects.filter(student_id=profile.pk).update(student_read=True)
            profile.update(student_online=F("student_online") + 1)
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        profile = Profile.objects.filter(user_id=self.scope["user"].pk)
        if profile[0].is_teacher:
            profile.update(teacher_online=F("teacher_online") - 1)
        elif profile[0].is_student:
            profile.update(student_online=F("teacher_online") - 1)
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        profile = Profile.objects.get(user_id=self.scope["user"].pk)
        if profile.is_teacher:
            if profile.student_online == 0:
                get_student = Messages.objects.filter(teacher_id=profile.pk).first()
                Messages.objects.create(
                    student_id=get_student.pk, 
                    teacher_id=profile.pk, 
                    to_student=message, 
                    student_read=False
                )
        elif profile.is_student:
            if profile.teacher_online == 0:
                get_teacher = Messages.objects.filter(student_id=profile.pk).first()
                Messages.objects.create(
                    student_id=profile.pk, 
                    teacher_id=get_teacher.pk, 
                    to_teacher=message, 
                    teacher_read=False
                )
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
