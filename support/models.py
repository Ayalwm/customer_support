from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, datetime

class Ticket(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def due_date(self):
        """Determine when the ticket should be escalated based on priority."""
        if self.priority == 'high':
            return self.created_at + timedelta(days=1)
        elif self.priority == 'medium':
            return self.created_at + timedelta(days=2)
        elif self.priority == 'low':
            return self.created_at + timedelta(days=3)
        return self.created_at


class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()  # 📧 Store user's email
    comment = models.TextField()
    rating = models.PositiveIntegerField(default=0)  # ⭐ Star rating (1-5)
    created_at = models.DateTimeField(auto_now_add=True)
