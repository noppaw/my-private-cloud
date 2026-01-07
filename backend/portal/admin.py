from django.contrib import admin
from .models import MicroApp

@admin.register(MicroApp)
class MicroAppAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)