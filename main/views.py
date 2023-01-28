from django.shortcuts import render

from main.models import Profile, Messages

def index(request):
    if request.user.is_authenticated and request.user.is_superuser is False:
        profile = Profile.objects.get(user_id=request.user.pk)
        messages_filter = dict()
        if profile.is_student:
            messages_filter['student_id'] = profile.pk
            messages_filter['student_read'] = False
        elif profile.is_teacher:
            messages_filter['teacher_id'] = profile.pk
            messages_filter['teacher_read'] = False
        unread_messages = Messages.objects.filter(**messages_filter).count()
        if unread_messages:
            context = {
                'user_is_authenticated': request.user.is_authenticated,
                'user_is_staff': request.user.is_superuser,
                'unread_messages_count': unread_messages,
                'room_name': 'test',
            }
            return render(request, "main/index.html", context)

    context = {
        'user_is_authenticated': request.user.is_authenticated, 
        'user_is_staff': request.user.is_superuser,
        'room_name': 'test',
    }
    return render(request, "main/index.html", context)
