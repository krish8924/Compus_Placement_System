from django.contrib import admin
from .models import JobCategory, JobPosting, JobApplication, Interview

@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'job_type', 'status', 'application_deadline', 'created_at')
    list_filter = ('status', 'job_type', 'created_at', 'application_deadline')
    search_fields = ('title', 'company__company_name', 'description')
    date_hierarchy = 'created_at'

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('student', 'job', 'status', 'applied_at')
    list_filter = ('status', 'applied_at')
    search_fields = ('student__user__username', 'job__title', 'job__company__company_name')
    date_hierarchy = 'applied_at'

@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ('application', 'date_time', 'interview_type', 'status')
    list_filter = ('status', 'interview_type', 'date_time')
    search_fields = ('application__student__user__username', 'application__job__title', 'interviewer')
    date_hierarchy = 'date_time'
