from celery import shared_task
from django.core.mail import send_mail
from django.utils.timezone import now, timedelta
from django.conf import settings  # Import Django settings
from .models import Ticket

@shared_task
def send_ticket_reminders():
    priority_timing = {
        'high': 1,
        'medium': 2,
        'low': 3
    }

    sent_count = 0

    for priority, days in priority_timing.items():
        overdue_tickets = Ticket.objects.filter(
            status='open',
            priority=priority,
            created_at__lte=now() - timedelta(days=days)
        )

        if not overdue_tickets.exists():
            print(f"No overdue tickets found for priority: {priority}")
            continue

        for ticket in overdue_tickets:
            if not ticket.email:
                print(f"Skipping Ticket {ticket.id}: No email provided.")
                continue

            print(f"Sending reminder to: {ticket.email}")

            subject = f"Reminder: Ticket '{ticket.title}' Needs Attention"
            message = f"Your ticket '{ticket.title}' is still open and requires resolution."

            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, [ticket.email])
                sent_count += 1
            except Exception as e:
                print(f"Failed to send email for Ticket {ticket.id}: {e}")

    return f"{sent_count} reminders sent."
