from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Line)
admin.site.register(Station)
admin.site.register(Route)
admin.site.register(Traffic)
admin.site.register(Journey)

# Hiding Unnecessary Models for this task
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

admin.site.unregister(User)
admin.site.unregister(Group)
