from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Avg, Max, Sum, Q
from django.utils import timezone

from .models import PlacementSeason, PlacementStatistics, Announcement, Event
from .forms import AnnouncementForm, EventForm, PlacementSeasonForm, PlacementStatisticsForm
from accounts.models import User, StudentProfile, CompanyProfile
from jobs.models import JobPosting, JobApplication, Interview


@login_required
def student_dashboard(request):
    """Dashboard for students"""
    if not request.user.is_student:
        messages.error(request, "You don't have access to the student dashboard.")
        return redirect('home')
    
    # Get student profile
    student = get_object_or_404(StudentProfile, user=request.user)
    
    # Get student's applications
    applications = JobApplication.objects.filter(student=student).select_related('job')
    
    # Get upcoming interviews
    upcoming_interviews = Interview.objects.filter(
        application__student=student,
        date_time__gte=timezone.now(),
        status='scheduled'
    ).order_by('date_time')
    
    # Get active job postings that match student's department
    matching_jobs = JobPosting.objects.filter(
        status='open',
        application_deadline__gte=timezone.now().date()
    ).order_by('-created_at')[:5]
    
    # Get announcements relevant to students
    announcements = Announcement.objects.filter(
        Q(audience='all') | Q(audience='students'),
        is_active=True,
    ).filter(
        Q(expires_at__isnull=True) | Q(expires_at__gte=timezone.now())
    ).order_by('-created_at')[:5]
    
    # Get upcoming events
    events = Event.objects.filter(
        date_time__gte=timezone.now(),
        is_active=True
    ).order_by('date_time')[:5]
    
    context = {
        'student': student,
        'applications': applications,
        'application_count': applications.count(),
        'interview_count': upcoming_interviews.count(),
        'upcoming_interviews': upcoming_interviews,
        'matching_jobs': matching_jobs,
        'announcements': announcements,
        'events': events,
    }
    
    return render(request, 'dashboard/student_dashboard.html', context)


@login_required
def company_dashboard(request):
    """Dashboard for companies"""
    if not request.user.is_company:
        messages.error(request, "You don't have access to the company dashboard.")
        return redirect('home')
    
    # Get company profile
    company = get_object_or_404(CompanyProfile, user=request.user)
    
    # Get company's job postings
    jobs = JobPosting.objects.filter(company=company)
    active_jobs = jobs.filter(status='open')
    
    # Get applications for company's jobs
    applications = JobApplication.objects.filter(job__company=company)
    recent_applications = applications.order_by('-applied_at')[:10]
    
    # Get upcoming interviews
    upcoming_interviews = Interview.objects.filter(
        application__job__company=company,
        date_time__gte=timezone.now()
    ).order_by('date_time')[:5]
    
    # Application statistics
    application_stats = {
        'total': applications.count(),
        'pending': applications.filter(status='applied').count(),
        'shortlisted': applications.filter(status='shortlisted').count(),
        'selected': applications.filter(status='selected').count(),
        'rejected': applications.filter(status='rejected').count(),
    }
    
    # Get announcements relevant to companies
    announcements = Announcement.objects.filter(
        Q(audience='all') | Q(audience='companies'),
        is_active=True,
    ).filter(
        Q(expires_at__isnull=True) | Q(expires_at__gte=timezone.now())
    ).order_by('-created_at')[:5]
    
    context = {
        'company': company,
        'active_jobs': active_jobs,
        'jobs_count': jobs.count(),
        'applications_stats': application_stats,
        'recent_applications': recent_applications,
        'upcoming_interviews': upcoming_interviews,
        'announcements': announcements,
    }
    
    return render(request, 'dashboard/company_dashboard.html', context)


@login_required
def officer_dashboard(request):
    """Dashboard for placement officers"""
    if not request.user.is_officer:
        messages.error(request, "You don't have access to the placement officer dashboard.")
        return redirect('home')
    
    # Get statistics for current placement season
    current_season = PlacementSeason.objects.filter(is_active=True).first()
    
    # Overall statistics
    total_companies = CompanyProfile.objects.count()
    total_students = StudentProfile.objects.count()
    total_jobs = JobPosting.objects.count()
    active_jobs = JobPosting.objects.filter(status='open').count()
    
    # Application statistics
    applications = JobApplication.objects.all()
    application_stats = {
        'total': applications.count(),
        'pending': applications.filter(status='applied').count(),
        'shortlisted': applications.filter(status='shortlisted').count(),
        'selected': applications.filter(status='selected').count(),
        'rejected': applications.filter(status='rejected').count(),
    }
    
    # Department-wise placement statistics
    if current_season:
        department_stats = PlacementStatistics.objects.filter(season=current_season)
    else:
        department_stats = []
    
    # Recent activities
    recent_jobs = JobPosting.objects.order_by('-created_at')[:5]
    recent_applications = JobApplication.objects.order_by('-applied_at')[:5]
    upcoming_interviews = Interview.objects.filter(date_time__gte=timezone.now()).order_by('date_time')[:5]
    
    # Get all announcements
    announcements = Announcement.objects.filter(is_active=True).order_by('-created_at')[:5]
    
    # Get upcoming events
    events = Event.objects.filter(date_time__gte=timezone.now(), is_active=True).order_by('date_time')[:5]
    
    context = {
        'current_season': current_season,
        'total_companies': total_companies,
        'total_students': total_students,
        'total_jobs': total_jobs,
        'active_jobs': active_jobs,
        'application_stats': application_stats,
        'department_stats': department_stats,
        'recent_jobs': recent_jobs,
        'recent_applications': recent_applications,
        'upcoming_interviews': upcoming_interviews,
        'announcements': announcements,
        'events': events,
    }
    
    return render(request, 'dashboard/officer_dashboard.html', context)


@login_required
def statistics(request):
    """View detailed placement statistics"""
    # Check if current season exists, otherwise redirect to create one
    current_season = PlacementSeason.objects.filter(is_active=True).first()
    if not current_season and request.user.is_officer:
        messages.info(request, "Please create a placement season first.")
        return redirect('create_season')
    
    # Get all seasons
    seasons = PlacementSeason.objects.all().order_by('-year')
    
    # Get selected season
    selected_season_id = request.GET.get('season')
    if selected_season_id:
        selected_season = get_object_or_404(PlacementSeason, id=selected_season_id)
    else:
        selected_season = current_season or (seasons.first() if seasons.exists() else None)
    
    # Department-wise statistics for selected season
    if selected_season:
        department_stats = PlacementStatistics.objects.filter(season=selected_season)
    else:
        department_stats = []
    
    # Job type distribution
    job_type_distribution = JobPosting.objects.filter(
        created_at__gte=selected_season.start_date if selected_season else '1900-01-01',
        created_at__lte=selected_season.end_date if selected_season else '2999-12-31'
    ).values('job_type').annotate(count=Count('id'))
    
    # Monthly job postings
    if selected_season:
        # This is a simplified example - in real implementation, you might use more complex queries
        monthly_jobs = JobPosting.objects.filter(
            created_at__gte=selected_season.start_date,
            created_at__lte=selected_season.end_date
        ).extra(
            select={'month': "EXTRACT(MONTH FROM created_at)"}
        ).values('month').annotate(count=Count('id')).order_by('month')
    else:
        monthly_jobs = []
    
    context = {
        'seasons': seasons,
        'selected_season': selected_season,
        'department_stats': department_stats,
        'job_type_distribution': job_type_distribution,
        'monthly_jobs': monthly_jobs
    }
    
    return render(request, 'dashboard/statistics.html', context)


@login_required
def create_announcement(request):
    """Create a new announcement"""
    if not request.user.is_officer:
        messages.error(request, "Only placement officers can create announcements.")
        return redirect('home')
    
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.created_by = request.user
            announcement.save()
            messages.success(request, "Announcement created successfully!")
            return redirect('officer_dashboard')
    else:
        form = AnnouncementForm()
    
    return render(request, 'dashboard/create_announcement.html', {'form': form})


@login_required
def create_event(request):
    """Create a new event"""
    if not request.user.is_officer:
        messages.error(request, "Only placement officers can create events.")
        return redirect('home')
    
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            messages.success(request, "Event created successfully!")
            return redirect('officer_dashboard')
    else:
        form = EventForm()
    
    return render(request, 'dashboard/create_event.html', {'form': form})


@login_required
def create_season(request):
    """Create a new placement season"""
    if not request.user.is_officer:
        messages.error(request, "Only placement officers can create placement seasons.")
        return redirect('home')
    
    if request.method == 'POST':
        form = PlacementSeasonForm(request.POST)
        if form.is_valid():
            new_season = form.save(commit=False)
            
            # If this season is active, set all others to inactive
            if new_season.is_active:
                PlacementSeason.objects.filter(is_active=True).update(is_active=False)
            
            new_season.save()
            messages.success(request, f"Placement season {new_season.year} created successfully!")
            return redirect('statistics')
    else:
        form = PlacementSeasonForm()
    
    return render(request, 'dashboard/create_season.html', {'form': form})


@login_required
def update_statistics(request, department=None):
    """Update placement statistics for a department"""
    if not request.user.is_officer:
        messages.error(request, "Only placement officers can update statistics.")
        return redirect('home')
    
    # Get current season
    current_season = get_object_or_404(PlacementSeason, is_active=True)
    
    # If department is provided, get existing stats or create new
    if department:
        stats, created = PlacementStatistics.objects.get_or_create(
            season=current_season,
            department=department
        )
    else:
        stats = None
    
    if request.method == 'POST':
        form = PlacementStatisticsForm(request.POST, instance=stats)
        if form.is_valid():
            form.save()
            messages.success(request, "Statistics updated successfully!")
            return redirect('statistics')
    else:
        form = PlacementStatisticsForm(instance=stats)
    
    context = {
        'form': form,
        'season': current_season,
        'department': department
    }
    
    return render(request, 'dashboard/update_statistics.html', context)
