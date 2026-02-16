from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db import transaction
from .models import StudentProfile, CompanyProfile, Notification
import datetime

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile_and_notification(sender, instance, created, **kwargs):
    """
    Create appropriate profile and welcome notification when a new user is created
    Handle in a transaction to ensure both succeed or fail together
    """
    if created:
        with transaction.atomic():
            # Create profile based on user type
            if instance.user_type == 'student' and not hasattr(instance, 'student_profile'):
                # Create student profile with default values
                current_year = datetime.datetime.now().year
                StudentProfile.objects.create(
                    user=instance,
                    roll_number=f"TEMP{instance.id}",  # Temporary roll number
                    department="Not Specified",  # Default department
                    year_of_graduation=current_year + 4  # Default graduation year (4 years from now)
                )
                welcome_message = "Welcome to the Campus Placement System! Complete your profile and upload your resume to start applying for jobs."
            
            elif instance.user_type == 'company' and not hasattr(instance, 'company_profile'):
                # Create company profile with minimal default values
                CompanyProfile.objects.create(
                    user=instance,
                    company_name=f"{instance.username}'s Company",  # Default company name 
                    industry="Not Specified",  # Default industry
                    description="Company description not provided yet.",  # Default description
                    website="https://example.com",  # Default website
                    address="Address not provided yet."  # Default address
                )
                welcome_message = "Welcome to the Campus Placement System! Complete your company profile to start posting job opportunities."
            
            elif instance.user_type == 'officer':
                welcome_message = "Welcome to the Campus Placement System! You have administrator privileges to manage the placement process."
            
            else:
                welcome_message = "Welcome to the Campus Placement System! Complete your profile to get started."
            
            # Create welcome notification
            Notification.objects.create(
                user=instance,
                title="Welcome to Campus Placement System",
                message=welcome_message
            )
