from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Teacher, User
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from phonenumber_field.formfields import PhoneNumberField


User = get_user_model()


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'first_name',
                  'last_name', 'is_student', 'is_teacher']


class TeacherProfileForm(ModelForm):
    phone_number = PhoneNumberField(
        error_messages={
            'invalid': 'Enter a valid phone number (e.g. 01711111111 or +8801711111111)'},
        required=False
    )

    class Meta:
        model = Teacher
        fields = ['designation', 'phone_number', 'time_table']


class UserProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'avatar']
