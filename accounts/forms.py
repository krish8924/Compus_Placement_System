from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, StudentProfile, CompanyProfile


class UserRegistrationForm(UserCreationForm):
    """Form for user registration with user type selection"""
    email = forms.EmailField()
    user_type = forms.ChoiceField(
        choices=User.USER_TYPE_CHOICES,
        widget=forms.RadioSelect,
        required=True
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'user_type']


class UserUpdateForm(forms.ModelForm):
    """Form for updating user details"""
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number']


class StudentProfileForm(forms.ModelForm):
    """Form for student profile details"""
    class Meta:
        model = StudentProfile
        fields = [
            'roll_number', 'department', 'year_of_graduation', 
            'cgpa', 'skills', 'bio', 'linkedin_profile', 'github_profile'
        ]
        widgets = {
            'skills': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Separate skills with commas'}),
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us about yourself'}),
        }


class CompanyProfileForm(forms.ModelForm):
    """Form for company profile details"""
    class Meta:
        model = CompanyProfile
        fields = [
            'company_name', 'industry', 'description', 
            'website', 'address', 'established_year'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }


class ResumeUploadForm(forms.ModelForm):
    """Form for uploading resume"""
    class Meta:
        model = StudentProfile
        fields = ['resume']
        widgets = {
            'resume': forms.FileInput(attrs={'accept': '.pdf,.doc,.docx'})
        }
        
    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume:
            # Validate file type
            file_extension = resume.name.split('.')[-1].lower()
            if file_extension not in ['pdf', 'doc', 'docx']:
                raise forms.ValidationError("Only PDF and Word documents are allowed")
            # Validate file size (5MB limit)
            if resume.size > 5 * 1024 * 1024:
                raise forms.ValidationError("File size must be under 5MB")
        return resume
