from django.contrib import admin
from . import models


# Admin panel customization for the TodoAdmin
@admin.register(models.Todo)
class TodoAdmin(admin.ModelAdmin):
    # Display fields on the Admin page
    list_display = ['title', 'content', 'priority', 'is_done']
