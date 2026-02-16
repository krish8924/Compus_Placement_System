from django.contrib import admin
from .models import PlacementSeason, PlacementStatistics, Announcement, Event

@admin.register(PlacementSeason)
class PlacementSeasonAdmin(admin.ModelAdmin):
    list_display = ('year', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('year',)

@admin.register(PlacementStatistics)
class PlacementStatisticsAdmin(admin.ModelAdmin):
    list_display = ('department', 'season', 'total_students', 'placed_students', 'placement_percentage', 'average_package')
    list_filter = ('season', 'department')
    search_fields = ('department',)

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'audience', 'created_by', 'created_at', 'is_active')
    list_filter = ('audience', 'is_active', 'created_at')
    search_fields = ('title', 'content')
    date_hierarchy = 'created_at'

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_time', 'company', 'created_by', 'is_active')
    list_filter = ('is_active', 'date_time')
    search_fields = ('title', 'description', 'company__company_name')
    date_hierarchy = 'date_time'
