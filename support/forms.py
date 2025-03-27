from django import forms
from .models import Ticket, Comment

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'priority', 'email', 'image_attachment', 'file_attachment']



class CommentForm(forms.ModelForm):
    RATING_CHOICES = [(i, f"{i} ⭐") for i in range(1, 6)]  # 1-5 stars
    
    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect, required=True)
     
    class Meta:
        model = Comment
        fields = ['email', 'comment', 'rating']  # 📧 Include email field
    
    def clean_rating(self):
        # Convert rating to integer before saving to the database
        return int(self.cleaned_data['rating'])
