from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.utils import timezone

from .models import JobPosting, JobApplication, Interview, JobCategory
from .forms import JobPostingForm, JobApplicationForm, InterviewForm
from accounts.models import StudentProfile, Notification
from accounts.utils import send_email
from django.contrib.auth import get_user_model
User = get_user_model()

@login_required
def job_list(request):
    """
   List all open job postings with filters
    """
    jobs = JobPosting.objects.filter(status='open')
    categories = JobCategory.objects.all()
    
    # Filter by category
    category_id = request.GET.get('category')
    if category_id:
        jobs = jobs.filter(category_id=category_id)
    
    # Filter by job type
    job_type = request.GET.get('job_type')
    if job_type:
        jobs = jobs.filter(job_type=job_type)
    
    # Filter by keyword search
    keyword = request.GET.get('keyword')
    if keyword:
        jobs = jobs.filter(
            Q(title__icontains=keyword) | 
            Q(description__icontains=keyword) |
            Q(company__company_name__icontains=keyword)
        )
    
    # Pagination
    paginator = Paginator(jobs, 10)  # Show 10 jobs per page
    page = request.GET.get('page')
    jobs = paginator.get_page(page)
    
    context = {
        'jobs': jobs,
        'categories': categories,
    }
    
    return render(request, 'jobs/job_list.html', context)


@login_required
def job_detail(request, job_id):
    """
    View details of a specific job posting and allow students to apply
    """
    job = get_object_or_404(JobPosting, id=job_id)
    
    # Check if user has already applied
    has_applied = False
    if request.user.is_student:
        student_profile = get_object_or_404(StudentProfile, user=request.user)
        has_applied = JobApplication.objects.filter(job=job, student=student_profile).exists()
    
    # Check if the job deadline has passed
    deadline_passed = job.application_deadline < timezone.now().date()
    
    if request.method == 'POST' and request.user.is_student and not has_applied and not deadline_passed:
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            student_profile = get_object_or_404(StudentProfile, user=request.user)
            application.job = job
            application.student = student_profile
            application.save()
            
            # EMAIL TO STUDENT
            send_email(
                subject="Job Application Submitted Successfully",
                message=(
                    f"Hi {request.user.first_name},\n\n"
                    f"You have successfully applied for the job:\n\n"
                    f"Job Title: {job.title}\n"
                    f"Company: {job.company.company_name}\n\n"
                    "Your application has been received successfully.\n"
                    "You will be notified when the application status changes.\n\n"
                    "Best Regards,\n"
                    "Campus Placement Cell"
                    ),
                    recipient=request.user.email
            )
            
            # Create notification for company
            Notification.objects.create(
                user=job.company.user,
                title=f"New Application for {job.title}",
                message=f"{request.user.get_full_name()} has applied for the {job.title} position."
            )
            
            messages.success(request, f"You have successfully applied for {job.title}")
            return redirect('job_list')
    else:
        form = JobApplicationForm()
    
    context = {
        'job': job,
        'form': form,
        'has_applied': has_applied,
        'deadline_passed': deadline_passed
    }
    
    return render(request, 'jobs/job_detail.html', context)


@login_required
def post_job(request):
    """
    Allow companies to post new job openings
    """
    if not request.user.is_company:
        messages.error(request, "Only companies can post jobs.")
        return redirect('home')
    
    if request.method == 'POST':
        form = JobPostingForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            company_profile = request.user.company_profile
            job.company = company_profile
            job.save()
            
            # Notify placement officers about new job
            placement_officers = User.objects.filter(user_type='officer')
            for officer in placement_officers:
                Notification.objects.create(
                    user=officer,
                    title=f"New Job Posted: {job.title}",
                    message=f"{company_profile.company_name} has posted a new job: {job.title}"
                )
            
            messages.success(request, f"Job posting for '{job.title}' has been created successfully!")
            return redirect('manage_jobs')
    else:
        form = JobPostingForm()
    
    context = {
        'form': form,
        'is_edit': False
    }
    
    return render(request, 'jobs/post_job.html', context)


@login_required
def edit_job(request, job_id):
    """
    Edit an existing job posting
    """
    if not request.user.is_company:
        messages.error(request, "Only companies can edit job postings.")
        return redirect('home')
    
    job = get_object_or_404(JobPosting, id=job_id, company=request.user.company_profile)
    
    if request.method == 'POST':
        form = JobPostingForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, f"Job posting for '{job.title}' has been updated successfully!")
            return redirect('manage_jobs')
    else:
        form = JobPostingForm(instance=job)
    
    context = {
        'form': form,
        'is_edit': True,
        'job': job
    }
    
    return render(request, 'jobs/post_job.html', context)


@login_required
def manage_jobs(request):
    """
    Allow companies to manage their job postings
    """
    if not request.user.is_company:
        messages.error(request, "Only companies can access job management.")
        return redirect('home')
    
    jobs = JobPosting.objects.filter(company=request.user.company_profile).order_by('-created_at')
    
    return render(request, 'jobs/manage_jobs.html', {'jobs': jobs})


@login_required
def applications(request):
    """
    View and manage job applications
    """
    if request.user.is_student:
        # Students view their applications
        student_profile = get_object_or_404(StudentProfile, user=request.user)
        applications = JobApplication.objects.filter(student=student_profile)
        template = 'jobs/student_applications.html'
    
    elif request.user.is_company:
        # Companies view applications for their jobs
        company_profile = request.user.company_profile
        applications = JobApplication.objects.filter(job__company=company_profile)
        template = 'jobs/company_applications.html'
    
    else:
        # Placement officers view all applications
        applications = JobApplication.objects.all()
        template = 'jobs/officer_applications.html'
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        applications = applications.filter(status=status)
    
    # Pagination
    paginator = Paginator(applications, 15)
    page = request.GET.get('page')
    applications = paginator.get_page(page)
    
    return render(request, template, {'applications': applications})


@login_required
def update_application_status(request, application_id):
    """
    Update the status of a job application
    """
    if not (request.user.is_company or request.user.is_officer):
        messages.error(request, "You don't have permission to update application status.")
        return redirect('home')
    
    application = get_object_or_404(JobApplication, id=application_id)
    
    # Only allow companies to update their own job applications
    if request.user.is_company and application.job.company != request.user.company_profile:
        messages.error(request, "You can only update applications for your jobs.")
        return redirect('applications')
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(JobApplication.STATUS_CHOICES).keys():
            old_status = application.status
            application.status = new_status
            application.save()
            
            # Notify the student about status change
            Notification.objects.create(
                user=application.student.user,
                title=f"Application Status Updated",
                message=f"Your application for {application.job.title} has been updated from {old_status} to {new_status}."
            )
            
            messages.success(request, f"Application status updated to {new_status}.")
        else:
            messages.error(request, "Invalid status provided.")
    
    return redirect('applications')


@login_required
def schedule_interview(request, application_id):
    """
    Schedule an interview for a job application
    """
    if not (request.user.is_company or request.user.is_officer):
        messages.error(request, "You don't have permission to schedule interviews.")
        return redirect('home')
    
    application = get_object_or_404(JobApplication, id=application_id)
    
    # Only allow companies to schedule interviews for their own job applications
    if request.user.is_company and application.job.company != request.user.company_profile:
        messages.error(request, "You can only schedule interviews for your jobs.")
        return redirect('applications')
    
    if request.method == 'POST':
        form = InterviewForm(request.POST)
        if form.is_valid():
            interview = form.save(commit=False)
            interview.application = application
            interview.save()

            student = application.student.user
            send_email(
                subject="📅 Interview Scheduled",
            message=(
                f"Hi {student.first_name},\n\n"
                f"Your interview has been scheduled.\n\n"
                f"Job Title: {application.job.title}\n"
                f"Company: {application.job.company.company_name}\n\n"
                f"Interview Details:\n"
                f"Date & Time: {interview.date_time}\n"
                f"Mode: {interview.interview_type}\n"
                f"Meeting Link: {interview.meeting_link}\n"
                f"Location: {interview.location}\n\n"
                "Please be available on time.\n\n"
                "All the best 👍\n"
                "Campus Placement Cell"
                ),
                recipient=student.email
                )
            
            # Update application status to shortlisted
            application.status = 'shortlisted'
            application.save()
            
            # Notify the student about the interview
            Notification.objects.create(
                user=application.student.user,
                title=f"Interview Scheduled for {application.job.title}",
                message=f"You have been scheduled for an interview on {interview.date_time}. Please check your interview details."
            )
            
            messages.success(request, "Interview has been scheduled successfully!")
            return redirect('applications')
    else:
        form = InterviewForm()
    
    context = {
        'form': form,
        'application': application
    }
    
    return render(request, 'jobs/schedule_interview.html', context)


@login_required
def interviews(request):
    """
    View scheduled interviews
    """
    if request.user.is_student:
        # Students view their interviews
        student_profile = get_object_or_404(StudentProfile, user=request.user)
        interviews = Interview.objects.filter(application__student=student_profile)
        template = 'jobs/student_interviews.html'
    
    elif request.user.is_company:
        # Companies view interviews for their job applications
        company_profile = request.user.company_profile
        interviews = Interview.objects.filter(application__job__company=company_profile)
        template = 'jobs/company_interviews.html'
    
    else:
        # Placement officers view all interviews
        interviews = Interview.objects.all()
        template = 'jobs/officer_interviews.html'
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        interviews = interviews.filter(status=status)
    
    # Filter by date range
    today = timezone.now().date()
    date_filter = request.GET.get('date_filter', 'upcoming')
    
    if date_filter == 'upcoming':
        interviews = interviews.filter(date_time__date__gte=today)
    elif date_filter == 'past':
        interviews = interviews.filter(date_time__date__lt=today)
    
    # Pagination
    paginator = Paginator(interviews, 10)
    page = request.GET.get('page')
    interviews = paginator.get_page(page)
    
    return render(request, template, {'interviews': interviews})


@login_required
def update_interview(request, interview_id):
    """
    Update interview details or provide feedback
    """
    if not (request.user.is_company or request.user.is_officer):
        messages.error(request, "You don't have permission to update interviews.")
        return redirect('home')
    
    interview = get_object_or_404(Interview, id=interview_id)
    
    # Only allow companies to update their own interviews
    if request.user.is_company and interview.application.job.company != request.user.company_profile:
        messages.error(request, "You can only update interviews for your jobs.")
        return redirect('interviews')
    
    if request.method == 'POST':
        form = InterviewForm(request.POST, instance=interview)
        if form.is_valid():
            form.save()
            
            # If interview status is updated to completed, notify the student
            if interview.status == 'completed':
                Notification.objects.create(
                    user=interview.application.student.user,
                    title="Interview Feedback Available",
                    message=f"Feedback for your interview with {interview.application.job.company.company_name} is now available."
                )
            
            messages.success(request, "Interview details updated successfully!")
            return redirect('interviews')
    else:
        form = InterviewForm(instance=interview)
    
    context = {
        'form': form,
        'interview': interview,
        'is_update': True
    }
    
    return render(request, 'jobs/update_interview.html', context)
