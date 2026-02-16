from django import forms
from .models import PlacementSeason, PlacementStatistics, Announcement, Event
from accounts.models import CompanyProfile

class PlacementSeasonForm(forms.ModelForm):
    """Form for creating a new placement season"""
    class Meta:
        model = PlacementSeason
        fields = ['year', 'start_date', 'end_date', 'is_active']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date and start_date >= end_date:
            raise forms.ValidationError("End date must be after start date.")
        
        return cleaned_data


class PlacementStatisticsForm(forms.ModelForm):
    """Form for updating placement statistics"""
    class Meta:
        model = PlacementStatistics
        fields = [
            'department', 'total_students', 'placed_students', 
            'highest_package', 'average_package', 'total_companies_visited'
        ]
    
    def clean(self):
        cleaned_data = super().clean()
        total_students = cleaned_data.get('total_students')
        placed_students = cleaned_data.get('placed_students')
        
        if total_students and placed_students and placed_students > total_students:
            raise forms.ValidationError("Placed students cannot be greater than total students.")
        
        return cleaned_data


class AnnouncementForm(forms.ModelForm):
    """Form for creating announcements"""
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'audience', 'expires_at', 'is_active']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
            'expires_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        
    def clean_expires_at(self):
        """Ensure timezone awareness for expires_at field"""
        expires_at = self.cleaned_data.get('expires_at')
        if expires_at:
            # If timezone is naive, make it timezone-aware
            if expires_at.tzinfo is None:
                from django.utils import timezone
                expires_at = timezone.make_aware(expires_at)
        return expires_at


class EventForm(forms.ModelForm):
    """Form for creating events"""
    class Meta:
        model = Event
        fields = ['title', 'description', 'date_time', 'location', 'company', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Sort companies alphabetically by company name
        self.fields['company'].queryset = CompanyProfile.objects.all().order_by('company_name')
        
    def clean_date_time(self):
        """Ensure timezone awareness for date_time field"""
        date_time = self.cleaned_data.get('date_time')
        if date_time:
            # If timezone is naive, make it timezone-aware
            if date_time.tzinfo is None:
                from django.utils import timezone
                date_time = timezone.make_aware(date_time)
        return date_time
