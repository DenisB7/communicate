from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_teacher = models.BooleanField(default=False)
    teacher_online = models.IntegerField(default=0)
    is_student = models.BooleanField(default=False)
    student_online = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.user


class Messages(models.Model):
    student = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='student')
    to_teacher = models.TextField()
    teacher_read = models.BooleanField()
    teacher = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='teacher')
    to_student = models.TextField()
    student_read = models.BooleanField()

    def __str__(self) -> str:
        return f"Student: {self.student.username} Teacher: {self.teacher.username}"
