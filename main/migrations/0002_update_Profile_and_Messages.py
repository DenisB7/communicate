# Generated by Django 4.1.5 on 2023-01-28 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messages',
            name='to_student',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='messages',
            name='to_teacher',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='student_online',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='profile',
            name='teacher_online',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
    ]