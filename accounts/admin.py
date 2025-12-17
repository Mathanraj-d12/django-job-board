from django.contrib import admin
from .models import Profile


# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'role']
    search_fields = ['user__username', 'role']
    list_filter = ['role']
    list_display_links = ['user']