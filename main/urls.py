from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views

urlpatterns = [
    path("", views.index, name="main"),
    path("login/", LoginView.as_view(template_name="templates/main/login.html"), name="login-user"),
    path("logout/", LogoutView.as_view(), name="logout-user"),
]
