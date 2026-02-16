from django.db import models
from django.conf import settings
from accounts.models import StudentProfile, CompanyProfile
from jobs.models import JobPosting, JobApplication


class PlacementSeason(models.Model):
    """
    Academic year for placement tracking
    """
    year = models.CharField(max_length=9, unique=True)  # e.g., "2023-2024"
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)
    
    def __str__(self):
        return self.year


class PlacementStatistics(models.Model):
    """
    Overall placement statistics for a season
    """
    season = models.ForeignKey(PlacementSeason, on_delete=models.CASCADE, related_name='statistics')
    department = models.CharField(max_length=100)
    total_students = models.PositiveIntegerField(default=0)
    placed_students = models.PositiveIntegerField(default=0)
    highest_package = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    average_package = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_companies_visited = models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together = ('season', 'department')
        verbose_name_plural = "Placement Statistics"
    
    def __str__(self):
        return f"{self.department} - {self.season.year}"
    
    @property
    def placement_percentage(self):
        if self.total_students > 0:
            return (self.placed_students / self.total_students) * 100
        return 0


class Announcement(models.Model):
    """
    System-wide announcements
    """
    AUDIENCE_CHOICES = (
        ('all', 'All Users'),
        ('students', 'Students Only'),
        ('companies', 'Companies Only'),
        ('officers', 'Placement Officers Only'),
    )
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    audience = models.CharField(max_length=20, choices=AUDIENCE_CHOICES, default='all')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class Event(models.Model):
    """
    Placement events such as pre-placement talks, workshops, etc.
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_time = models.DateTimeField()
    location = models.CharField(max_length=200)
    company = models.ForeignKey(CompanyProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='events')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-date_time']
    
    def __str__(self):
        return self.title
