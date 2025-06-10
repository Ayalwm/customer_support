from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

from .forms import TicketForm, CommentForm

from .models import Ticket, Comment
from django.contrib.auth.models import AnonymousUser
from chat.models import Message 
from .models import Ticket
from chat.models import Message 

def ticket_list(request):
    tickets = Ticket.objects.none()

    if request.user.is_authenticated:
        if request.user.is_staff:
            tickets = Ticket.objects.all()
        else:
            tickets = Ticket.objects.filter(created_by=request.user)

        # Attach related chat messages to each ticket
        for ticket in tickets:
            ticket.chat_messages = Message.objects.filter(ticket=ticket).select_related('sender').order_by('timestamp')

    return render(request, 'support/ticket_list.html', {'tickets': tickets})

def all_reviews(request):
    reviews = Comment.objects.all()  # Get all comments/reviews from the database

    # Calculate filled and empty stars for each review
    for review in reviews:
        review.stars_filled = list(range(1, review.rating + 1))  # Filled stars
        review.stars_empty = list(range(review.rating + 1, 6))  # Empty stars

    return render(request, 'support/all_reviews.html', {'reviews': reviews})

def ticket_comment(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    # Allow anyone to comment, even guests
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            # If the user is logged in, associate the comment with the logged-in user
            if isinstance(request.user, AnonymousUser):
                user = None  # Set user as None for anonymous comments
            else:
                user = request.user  # Otherwise, associate with the logged-in user

            # Save the comment, including the rating
            Comment.objects.create(
                ticket=ticket,
                user=user,
                email=form.cleaned_data["email"],  # ✅ Ensure email is stored
                comment=form.cleaned_data["comment"],
                rating=form.cleaned_data["rating"]  # Save the rating
            )

            messages.success(request, "Your comment has been submitted successfully.")
            return redirect("ticket_list")
    else:
        form = CommentForm()

    return render(request, "support/ticket_comment.html", {
        "form": form,
        "ticket": ticket,
        "max_rating": 5,  # Pass the max rating value to the template
    })

def send_ticket_update_email(ticket):
    # if not ticket.email:
    #     print("⚠️ Error: Ticket has no email!")  # Debugging
    #     return  # Stop execution if no email is provided

    ticket = Ticket.objects.last()  # Get latest ticket
    print(f"Ticket Email: {ticket.email}")  # Should NOT be empty

    comment_url = settings.SITE_URL + reverse('ticket_comment', args=[ticket.id])
    recipient_email = ticket.email  

    subject = f"Ticket Status Updated: {ticket.title}"
    message = (
        f"Hello,\n\n"
        f"Your ticket '{ticket.title}' status has been updated to: {ticket.get_status_display()}.\n\n"
        f"If you have any comments, please click the link below to respond:\n"
        f"{comment_url}\n\n"
        f"Thank you,\nSupport Team"
    )

    try:
        print(f"Sending email to {recipient_email}...")  # Debugging
        result = send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient_email])
        print(f"Email send result: {result}")  # Should print `1` if successful
    except Exception as e:
        print(f"Email sending failed: {e}")  # Debugging

def is_admin(user):
    return user.is_staff
def create_ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)  # ✅ Handling file uploads
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user if request.user.is_authenticated else None
            ticket.email = request.POST.get('email', '')

            # ✅ Debugging: Check if Django receives the file
            if "image_attachment" in request.FILES:
                print(f"✅ Received Image: {request.FILES['image_attachment'].name}")
            else:
                print("❌ No Image Received")

            if "file_attachment" in request.FILES:
                print(f"✅ Received File: {request.FILES['file_attachment'].name}")
            else:
                print("❌ No File Received")

            ticket.save()
            messages.success(request, "Your ticket has been created successfully!")
            return redirect("ticket_list")
        else:
            print("❌ Form Errors:", form.errors)  # Debugging
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
