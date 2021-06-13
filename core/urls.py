from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls import static
from .views import home, teacherProfile, viewRoutine, createRoutine, registerCourse, registerRoom
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', home, name="home"),
    path('profile/', teacherProfile, name="teacher_profile"),
    path('admin-dash/', viewRoutine, name="admin_dash"),
    path('view-routine/', viewRoutine, name="view_routine"),
    path('create-routine/', createRoutine, name="create_routine"),
    path('course-register/', registerCourse, name="course_register"),
    path('room-register/', registerRoom, name="room_register"),

]
