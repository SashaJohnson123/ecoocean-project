from django.contrib import admin
from .models import Project, Pledge, Category

admin.site.register(Project)
admin.site.register(Pledge)
admin.site.register(Category)
