from django import forms
from appweb.models import UserFollows, Ticket, Review
from django.shortcuts import get_object_or_404
from authentication.models import User


class FollowingForm(forms.Form):
    username = forms.CharField(max_length=128, label="",
                               widget=forms.TextInput(attrs={'placeholder': "Nom d'utilisateur"}))


class TicketCreation(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']

    def customSave(self, user):
        instance_ticket = self.save(commit=False)
        instance_ticket.user = user
        instance_ticket.save()
        return instance_ticket


class ReviewCreation(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body', 'ticket']
        labels = {
            'headline': "Titre",
            'rating': "Note",
            'body': "Commentaire",
        }
        widgets = {
            'ticket': forms.HiddenInput(attrs={'type': 'hidden'})
        }


class ReviewCreationWithoutTicket(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']
        labels = {
            'headline': "Titre",
            'rating': "Note",
            'body': "Commentaire",
        }

