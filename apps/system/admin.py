from django.contrib import admin
from .models import *

@admin.register(FormalBug)
class ProjectAdmin(admin.ModelAdmin):
    """现网bug"""
    list_display = ['project','question','reason','discoverer','solve_time']

@admin.register(SyetemQuestion)
class ProjectAdmin(admin.ModelAdmin):
    """系统问题"""
    list_display = ['project','question','handle']

