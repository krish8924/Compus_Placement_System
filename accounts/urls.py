from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    # Replace built-in LogoutView with our custom logout_view
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    
    # Password reset URLs
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), 
         name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), 
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), 
         name='password_reset_confirm'),
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), 
         name='password_reset_complete'),
    
    # Profile URLs
    path('profile/student/', views.student_profile, name='student_profile'),
    path('profile/company/', views.company_profile, name='company_profile'),
    path('resume-builder/', views.resume_builder, name='resume_builder'),
    
    # Notification URLs
    path('notifications/', views.notifications, name='notifications'),
]