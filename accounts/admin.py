from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, StudentProfile, CompanyProfile, Notification

# User admin with custom fields
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('user_type', 'phone_number')}),
    )
    list_filter = UserAdmin.list_filter + ('user_type',)
    list_display = ('username', 'email', 'user_type', 'first_name', 'last_name', 'is_staff')

admin.site.register(User, CustomUserAdmin)

# Student Profile Admin
@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'roll_number', 'department', 'year_of_graduation', 'cgpa')
    search_fields = ('user__username', 'roll_number', 'department')
    list_filter = ('department', 'year_of_graduation')

# Company Profile Admin
@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user', 'industry', 'website')
    search_fields = ('company_name', 'user__username', 'industry')
    list_filter = ('industry',)

# Notification Admin
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'read')
    list_filter = ('read', 'created_at')
    search_fields = ('title', 'message', 'user__username')
