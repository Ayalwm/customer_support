from celery import shared_task
from django.core.mail import send_mail
from django.utils.timezone import now, timedelta
from django.contrib.auth import get_user_model
from .models import Ticket

@shared_task
def send_ticket_reminders():
    priority_timing = {
        'high': 1,  # 1 day
        'medium': 2,  # 2 days
        'low': 3   # 3 days
    }

    User = get_user_model()  # Get the user model dynamically

    for priority, days in priority_timing.items():
        overdue_tickets = Ticket.objects.filter(
            status='open',
            priority=priority,
            created_at__lte=now() - timedelta(days=days)
        )

        for ticket in overdue_tickets:
            subject = f"Reminder: Ticket '{ticket.title}' Needs Attention"
            message = f"Your ticket '{ticket.title}' is still open and requires resolution."
            recipient_list = [ticket.created_by.email]

            # Notify the ticket owner
            send_mail(subject, message, 'support@example.com', recipient_list)

            # Notify the admins
            admin_emails = [admin.email for admin in User.objects.filter(is_staff=True)]
            send_mail(subject, f"Ticket '{ticket.title}' is still unresolved.", 'support@example.com', admin_emails)

    return f"{overdue_tickets.count()} reminders sent."
