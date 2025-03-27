import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "customer_support.settings")  # Replace with your actual project name
django.setup()

from django.contrib.auth.models import User
from support.models import Ticket, Comment  # Ensure this matches your app's models

def seed_database():
    # Create a normal user
    if not User.objects.filter(username='user').exists():
        user = User.objects.create_user(username='user', password='user1234')
        print("User 'user' created with password 'user1234'")
    else:
        user = User.objects.get(username='user')
        print("User 'user' already exists")

    # Create a superuser
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser(username='admin', password='admin1234', email='admin@example.com')
        print("Superuser 'admin' created with password 'admin1234'")
    else:
        admin = User.objects.get(username='admin')
        print("Superuser 'admin' already exists")

    # Create a ticket
    if not Ticket.objects.filter(title="Sample Ticket").exists():
        ticket = Ticket.objects.create(
            title="Sample Ticket",
            description="This is a test ticket created during Docker initialization.",
            priority="medium",
            status="open",
            created_by=user,
            email="user@example.com"
        )
        print("Sample ticket created.")
    else:
        ticket = Ticket.objects.get(title="Sample Ticket")
        print("Sample ticket already exists.")

    # Create a comment for the ticket
    if not Comment.objects.filter(ticket=ticket).exists():
        Comment.objects.create(
            ticket=ticket,
            user=user,
            email="user@example.com",
            comment="This is a test comment on the sample ticket.",
            rating=5
        )
        print("Sample comment created.")
    else:
        print("Sample comment already exists.")

if __name__ == '__main__':
    seed_database()
