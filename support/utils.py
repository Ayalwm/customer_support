from django.core.mail import send_mail
from django.conf import settings

def send_ticket_update_email(ticket):
    subject = f"Ticket Status Updated: {ticket.title}"
    message = (
        f"Hello {ticket.created_by.username},\n\n"
        f"Your ticket '{ticket.title}' status has been updated to: {ticket.get_status_display()}.\n\n"
        f"If you have any comments or feedback, please reply in the system.\n\n"
        f"Thank you,\nSupport Team"
    )
    recipient_email = ticket.created_by.email

    send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient_email])
