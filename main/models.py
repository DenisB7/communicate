from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_teacher = models.BooleanField(default=False)
    teacher_online = models.PositiveIntegerField(default=0, blank=True)
    is_student = models.BooleanField(default=False)
    student_online = models.PositiveIntegerField(default=0, blank=True)

    def __str__(self) -> str:
        if self.is_teacher:
            return f"Teacher: {self.user.username}"
        elif self.is_student:
            return f"Student: {self.user.username}"
        else:
            return f"Please set {self.user.username} as a teacher or student"


class Messages(models.Model):
    student = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='student')
    to_teacher = models.TextField(blank=True)
    teacher_read = models.BooleanField()
    teacher = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='teacher')
    to_student = models.TextField(blank=True)
    student_read = models.BooleanField()

    def __str__(self) -> str:
        return f"Student: {self.student.username} Teacher: {self.teacher.username}"
