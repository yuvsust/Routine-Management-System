from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls import static
from .views import home, teacherProfile, viewRoutine
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name="home"),
    path('profile/', teacherProfile, name="teacher_profile"),
    path('view-routine/', viewRoutine, name="view_routine"),
]
