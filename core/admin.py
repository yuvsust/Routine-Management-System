from django.contrib import admin
from .models import Course, Room, Class, RoomEngagement


admin.site.register(Course)
admin.site.register(Room)
admin.site.register(Class)
admin.site.register(RoomEngagement)
