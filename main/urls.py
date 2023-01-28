from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from main.views import index

urlpatterns = [
    path("", index, name="main"),
    path("login", LoginView.as_view(template_name="main/login.html"), name="login-user"),
    path("logout", LogoutView.as_view(), name="logout-user"),
]
