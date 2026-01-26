from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'is_completed', 'notify_telegram')
    list_filter = ('is_completed', 'notify_telegram', 'created_at')
    search_fields = ('title', 'description')
    date_hierarchy = 'start_time'