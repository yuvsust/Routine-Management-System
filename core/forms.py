from django import forms
from .models import Course, Room


class CourseRegisterForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'


class RoomRegisterForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
