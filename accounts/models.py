from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import os
import uuid

class User(AbstractUser):
    """
    Custom User model with additional fields for user type
    """
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('company', 'Company'),
        ('officer', 'Placement Officer'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
    
    def __str__(self):
        return self.username
    
    @property
    def is_student(self):
        return self.user_type == 'student'
    
    @property
    def is_company(self):
        return self.user_type == 'company'
    
    @property
    def is_officer(self):
        return self.user_type == 'officer'


def resume_upload_path(instance, filename):
    """Generate a unique file path for uploaded resumes"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('resumes', str(instance.user.id), filename)


class StudentProfile(models.Model):
    """
    Student profile containing academic and personal details
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    roll_number = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    year_of_graduation = models.IntegerField()
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    resume = models.FileField(upload_to=resume_upload_path, null=True, blank=True)
    skills = models.TextField(blank=True)
    bio = models.TextField(blank=True)
    linkedin_profile = models.URLField(blank=True)
    github_profile = models.URLField(blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"


class CompanyProfile(models.Model):
    """
    Company profile containing details about the recruiting company
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='company_profile')
    company_name = models.CharField(max_length=200)
    industry = models.CharField(max_length=100)
    description = models.TextField()
    website = models.URLField()
    address = models.TextField()
    established_year = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return self.company_name


class Notification(models.Model):
    """
    System notifications for users
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
