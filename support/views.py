from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

from .forms import TicketForm, CommentForm

from .models import Ticket, Comment

def is_admin(user):
    return user.is_staff

@login_required
def ticket_comment(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    # Only allow the ticket creator to comment (not admin)
    if request.user != ticket.created_by:
        messages.error(request, "You can only comment on your own tickets.")
        return redirect("ticket_list")

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment.objects.create(
                ticket=ticket,
                user=request.user,
                comment=form.cleaned_data["comment"]
            )
            messages.success(request, "Your comment has been submitted successfully.")
            return redirect("ticket_list")
    else:
        form = CommentForm()

    return render(request, "support/ticket_comment.html", {"form": form, "ticket": ticket})

def send_ticket_update_email(ticket):
    comment_url = settings.SITE_URL + reverse('ticket_comment', args=[ticket.id])
    
    subject = f"Ticket Status Updated: {ticket.title}"
    message = (
        f"Hello {ticket.created_by.username},\n\n"
        f"Your ticket '{ticket.title}' status has been updated to: {ticket.get_status_display()}.\n\n"
        f"If you have any comments, please click the link below to respond:\n"
        f"{comment_url}\n\n"
        f"Thank you,\nSupport Team"
    )
    
    recipient_email = ticket.created_by.email

    send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient_email])

@login_required
def ticket_list(request):
    if request.user.is_staff:  # Check if the user is an admin
        tickets = Ticket.objects.all()  # Admins see all tickets
    else:
        tickets = Ticket.objects.filter(created_by=request.user)  # Regular users see only their tickets
    
    return render(request, 'support/ticket_list.html', {'tickets': tickets})
@login_required
def create_ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()
            messages.success(request, "Your ticket has been created successfully!")
            return redirect("ticket_list")
    else:
        form = TicketForm()
    return render(request, "support/create_ticket.html", {"form": form})

@user_passes_test(is_admin)  # ✅ Allow only admins to update tickets
@login_required
def update_ticket_status(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == "POST":
        ticket.status = request.POST.get("status")
        ticket.save()

        # ✅ Send email after status update
        send_ticket_update_email(ticket)

        messages.success(request, "Ticket status updated, and user notified.")
        return redirect("ticket_list")

    return render(request, "support/update_ticket.html", {"ticket": ticket})
