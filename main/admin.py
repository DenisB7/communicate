from django.contrib import admin

from main.models import Profile, MessagesUnread


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass

@admin.register(MessagesUnread)
class MessagesUnreadAdmin(admin.ModelAdmin):
    pass
