from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Teacher, User
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


User = get_user_model()


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'first_name',
                  'last_name', 'is_student', 'is_teacher']


class TeacherProfileForm(ModelForm):
    class Meta:
        model = Teacher
        fields = ['designation', 'time_table']


class UserProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'avatar']
