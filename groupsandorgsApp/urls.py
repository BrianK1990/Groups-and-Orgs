from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("register", views.register),
    path("login", views.login),
    path("groups", views.groups),
    path("submitorg", views.submitorg),
    path("groups/<orgID>", views.groupinfo),
    path("joingroup/<orgID>", views.joingroup),
    path("leavegroup/<orgID>", views.leavegroup),
    path("logout", views.logout),
    path("dashboard", views.dashboard),
 ]
