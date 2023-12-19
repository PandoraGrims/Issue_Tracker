from django.contrib import admin
from .models import Status, Type, Task, Project

admin.site.register(Project)
admin.site.register(Status)
admin.site.register(Type)
admin.site.register(Task)
