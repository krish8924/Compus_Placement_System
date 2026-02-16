from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from .models import User, StudentProfile, CompanyProfile, Notification
from .forms import (
    UserRegistrationForm, StudentProfileForm, CompanyProfileForm, 
    UserUpdateForm, ResumeUploadForm
)
def register(request):
    """
    Handle user registration with different user types
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Note: Profile creation is now handled by signals.py
            # No need to manually create profiles here
            
            # Log the user in
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            
            messages.success(request, f'Account created for {username}! Please complete your profile.')
            
            # Redirect to appropriate profile completion page
            if user.user_type == 'student':
                return redirect('student_profile')
            elif user.user_type == 'company':
                return redirect('company_profile')
            else:
                return redirect('home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})
@login_required
def student_profile(request):
    """
    Handle student profile creation and updates
    """
    if request.user.user_type != 'student':
        messages.error(request, "You don't have access to this page.")
        return redirect('home')
    
    # Try to get existing profile, or initialize with default values if creating new one
    try:
        profile = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        # Create with default values for required fields
        profile = StudentProfile(
            user=request.user,
            roll_number='TBD',  # Temporary default value
            department='Not specified',  # Temporary default value
            year_of_graduation=2025  # Default graduation year
        )
        profile.save()
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = StudentProfileForm(request.POST, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('student_dashboard')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = StudentProfileForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': profile
    }
    
    return render(request, 'accounts/profile.html', context)
@login_required
def company_profile(request):
    """
    Handle company profile creation and updates
    """
    if request.user.user_type != 'company':
        messages.error(request, "You don't have access to this page.")
        return redirect('home')
    
    profile = CompanyProfile.objects.get_or_create(user=request.user)[0]
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = CompanyProfileForm(request.POST, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your company profile has been updated successfully!')
            return redirect('company_dashboard')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = CompanyProfileForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': profile
    }
    
    return render(request, 'accounts/profile.html', context)
@login_required
def resume_builder(request):
    """
    Resume builder and uploader for students
    """
    if request.user.user_type != 'student':
        messages.error(request, "Only students can access the resume builder.")
        return redirect('home')
    
    profile = get_object_or_404(StudentProfile, user=request.user)
    
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your resume has been updated successfully!')
            return redirect('student_dashboard')
    else:
        form = ResumeUploadForm(instance=profile)
    
    return render(request, 'accounts/resume_builder.html', {'form': form})
@login_required
def notifications(request):
    """View all notifications"""
    user_notifications = request.user.notifications.all()
    
    # Mark all as read
    unread = user_notifications.filter(read=False)
    if unread:
        unread.update(read=True)
    
    return render(request, 'accounts/notifications.html', {
        'notifications': user_notifications
    })
@login_required
def logout_view(request):
    """Handle user logout and clear session"""
    # Clear all session data
    request.session.flush()
    
    # Log the user out
    logout(request)
    
    # Redirect to login page
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')