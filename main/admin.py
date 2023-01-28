from django.contrib import admin

from main.models import Profile, Messages


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):
    pass
