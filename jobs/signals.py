from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import JobApplication
from accounts.utils import send_email
from accounts.models import Notification


@receiver(pre_save, sender=JobApplication)
def job_application_status_email(sender, instance, **kwargs):
    if not instance.pk:
        return  # new application, ignore

    old = JobApplication.objects.get(pk=instance.pk)

    if old.status != instance.status:
        student = instance.student.user
        job = instance.job

        # DATABASE notification
        Notification.objects.create(
            user=student,
            title="Application Status Updated",
            message=f"Your application for {job.title} is now '{instance.status}'."
        )

        # STATUS-SPECIFIC MESSAGE
        if instance.status == 'selected':
            subject = "🎉 Congratulations! You Are Selected"
            message = (
                f"Hi {student.first_name},\n\n"
                f"Congratulations! 🎉\n\n"
                f"You have been SELECTED for:\n"
                f"Job Title: {job.title}\n"
                f"Company: {job.company.company_name}\n\n"
                "The company or placement team will contact you soon.\n\n"
                "Best Wishes,\n"
                "Campus Placement Cell"
            )

        elif instance.status == 'rejected':
            subject = "Application Status Update"
            message = (
                f"Hi {student.first_name},\n\n"
                f"We regret to inform you that your application for:\n"
                f"{job.title} at {job.company.company_name}\n"
                f"has been rejected.\n\n"
                "Keep applying — success is near 💪\n\n"
                "Campus Placement Cell"
            )

        else:
            subject = "Application Status Updated"
            message = (
                f"Hi {student.first_name},\n\n"
                f"Your application status has been updated.\n\n"
                f"Job: {job.title}\n"
                f"Company: {job.company.company_name}\n"
                f"New Status: {instance.status}\n\n"
                "Login to your dashboard for more details.\n\n"
                "Campus Placement Cell"
            )

        send_email(subject, message, student.email)
