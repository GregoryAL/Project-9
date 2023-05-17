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
    ratingcustom = forms.ChoiceField(
        label='Note',
        widget=forms.RadioSelect(attrs={'class': 'rate'}),
        initial=0,
        choices=[
            (0, "0"),
            (1, "1"),
            (2, "2"),
            (3, "3"),
            (4, "4"),
            (5, "5")
        ]
    )
    class Meta:
        model = Review
        fields = ['headline', 'body', 'ticket']
        labels = {
            'headline': "Titre",
            'body': "Commentaire",
        }
        widgets = {
            'ticket': forms.HiddenInput(attrs={'type': 'hidden'})
        }
    def customSave(self, user, ratingcustom):
        instanceReview = self.save(commit=False)
        instanceReview.user = user
        instanceReview.rating = ratingcustom
        instanceReview.save()
        return instanceReview


class ReviewCreationWithoutTicket(forms.ModelForm):
    ratingcustom = forms.ChoiceField(
        label='Note',
        widget=forms.RadioSelect(attrs={'class': 'rate'}),
        initial=0,
        choices=[
            (0, "0"),
            (1, "1"),
            (2, "2"),
            (3, "3"),
            (4, "4"),
            (5, "5")
        ]
    )
    class Meta:
        model = Review
        fields = ['headline', 'body']
        labels = {
            'headline': "Titre",
            'body': "Commentaire",
        }

