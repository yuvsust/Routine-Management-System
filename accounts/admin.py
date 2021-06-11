from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Teacher, Student, TimeTable, TeacherEngagement


admin.site.register(User)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(TimeTable)
admin.site.register(TeacherEngagement)
