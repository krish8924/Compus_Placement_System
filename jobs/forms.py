from django import forms
from django.utils import timezone
from .models import JobPosting, JobApplication, Interview, JobCategory

class JobPostingForm(forms.ModelForm):
    """Form for creating and editing job postings"""
    
    class Meta:
        model = JobPosting
        fields = [
            'title', 'category', 'job_type', 'description', 
            'requirements', 'responsibilities', 'location', 
            'salary_range', 'application_deadline', 
            'positions_available', 'status', 'min_cgpa'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'requirements': forms.Textarea(attrs={'rows': 5}),
            'responsibilities': forms.Textarea(attrs={'rows': 5}),
            'application_deadline': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def clean_application_deadline(self):
        deadline = self.cleaned_data.get('application_deadline')
        if deadline < timezone.now().date():
            raise forms.ValidationError("Deadline cannot be in the past.")
        return deadline
    
    def clean_positions_available(self):
        positions = self.cleaned_data.get('positions_available')
        if positions <= 0:
            raise forms.ValidationError("Number of positions must be positive.")
        return positions


class JobApplicationForm(forms.ModelForm):
    """Form for students to apply for jobs"""
    
    class Meta:
        model = JobApplication
        fields = ['cover_letter']
        widgets = {
            'cover_letter': forms.Textarea(
                attrs={
                    'rows': 6, 
                    'placeholder': 'Explain why you are interested in this position and why you would be a good fit...'
                }
            ),
        }


class InterviewForm(forms.ModelForm):
    """Form for scheduling and updating interviews"""
    
    class Meta:
        model = Interview
        fields = [
            'date_time', 'location', 'interview_type', 
            'interviewer', 'notes', 'meeting_link', 'status', 'feedback'
        ]
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
            'feedback': forms.Textarea(attrs={'rows': 3}),
        }
    
    def clean_date_time(self):
        date_time = self.cleaned_data.get('date_time')
        if date_time < timezone.now():
            raise forms.ValidationError("Interview time cannot be in the past.")
        return date_time
    
    def clean(self):
        cleaned_data = super().clean()
        interview_type = cleaned_data.get('interview_type')
        location = cleaned_data.get('location')
        meeting_link = cleaned_data.get('meeting_link')
        
        if interview_type == 'online' and not meeting_link:
            self.add_error('meeting_link', "Meeting link is required for online interviews.")
        
        if interview_type == 'in_person' and not location:
            self.add_error('location', "Location is required for in-person interviews.")
        
        return cleaned_data
