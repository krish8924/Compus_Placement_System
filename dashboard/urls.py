from django.urls import path
from . import views

urlpatterns = [
    # Dashboard pages
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('company/', views.company_dashboard, name='company_dashboard'),
    path('officer/', views.officer_dashboard, name='officer_dashboard'),
    
    # Statistics
    path('statistics/', views.statistics, name='statistics'),
    path('season/create/', views.create_season, name='create_season'),
    path('statistics/update/<str:department>/', views.update_statistics, name='update_statistics'),
    
    # Announcements and Events
    path('announcement/create/', views.create_announcement, name='create_announcement'),
    path('event/create/', views.create_event, name='create_event'),
]
