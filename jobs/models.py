from django.db import models
from django.conf import settings
from accounts.models import CompanyProfile, StudentProfile

class JobCategory(models.Model):
    """
    Categories for job postings (e.g., Software Development, Data Science)
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Job Categories"
    
    def __str__(self):
        return self.name


class JobPosting(models.Model):
    """
    Job postings created by companies
    """
    JOB_TYPE_CHOICES = (
        ('full_time', 'Full Time'),
        ('internship', 'Internship'),
        ('part_time', 'Part Time'),
    )
    
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('draft', 'Draft'),
    )
    
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name='job_postings')
    title = models.CharField(max_length=200)
    category = models.ForeignKey(JobCategory, on_delete=models.SET_NULL, null=True, related_name='jobs')
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    description = models.TextField()
    requirements = models.TextField()
    responsibilities = models.TextField()
    location = models.CharField(max_length=100)
    salary_range = models.CharField(max_length=100, blank=True)
    application_deadline = models.DateField()
    positions_available = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    min_cgpa = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} at {self.company.company_name}"
    
    @property
    def is_active(self):
        return self.status == 'open'


class JobApplication(models.Model):
    """
    Applications submitted by students for job postings
    """
    STATUS_CHOICES = (
        ('applied', 'Applied'),
        ('under_review', 'Under Review'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('selected', 'Selected'),
    )
    
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='applications')
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    cover_letter = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('job', 'student')
        ordering = ['-applied_at']
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.job.title}"


class Interview(models.Model):
    """
    Interviews scheduled for job applications
    """
    INTERVIEW_TYPE_CHOICES = (
        ('online', 'Online'),
        ('in_person', 'In Person'),
        ('phone', 'Phone'),
    )
    
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('rescheduled', 'Rescheduled'),
    )
    
    application = models.ForeignKey(JobApplication, on_delete=models.CASCADE, related_name='interviews')
    date_time = models.DateTimeField()
    location = models.CharField(max_length=200, blank=True)
    interview_type = models.CharField(max_length=20, choices=INTERVIEW_TYPE_CHOICES)
    interviewer = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    meeting_link = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    feedback = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['date_time']
    
    def __str__(self):
        return f"Interview for {self.application} on {self.date_time}"
