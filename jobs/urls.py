from django.urls import path
from . import views

urlpatterns = [
    # Job Postings
    path('', views.job_list, name='job_list'),
    path('<int:job_id>/', views.job_detail, name='job_detail'),
    path('post/', views.post_job, name='post_job'),
    path('edit/<int:job_id>/', views.edit_job, name='edit_job'),
    path('manage/', views.manage_jobs, name='manage_jobs'),
    
    # Applications
    path('applications/', views.applications, name='applications'),
    path('applications/<int:application_id>/update/', 
         views.update_application_status, name='update_application'),
    
    # Interviews
    path('interviews/', views.interviews, name='interviews'),
    path('applications/<int:application_id>/schedule-interview/', 
         views.schedule_interview, name='schedule_interview'),
    path('interviews/<int:interview_id>/update/', 
         views.update_interview, name='update_interview'),
]
