from django.contrib import admin
from .models import Job, JobApplication


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'employer', 'location', 'employment_type', 'created_at']
    search_fields = ['title', 'employer__username', 'location']
    list_filter = ['employment_type', 'location', 'created_at']
    list_display_links = ['title']
    readonly_fields = ['created_at']


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['id', 'job', 'applicant', 'status', 'applied_at']
    search_fields = ['job__title', 'applicant__user__username']
    list_filter = ['status', 'applied_at']
    readonly_fields = ['applied_at']
