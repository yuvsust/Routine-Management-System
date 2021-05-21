from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Teacher, Student, TimeTable, Engagement


admin.site.register(User)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(TimeTable)
admin.site.register(Engagement)
