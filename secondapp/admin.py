from django.contrib import admin

from .models import Room,Topic,Messages

admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Messages)
# Register your models here.
    