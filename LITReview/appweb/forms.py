from django import forms
from appweb.models import UserFollows, Ticket, Review


class FollowingForm(forms.Form):
    # Following form include 1 field for username
    username = forms.CharField(max_length=128, label="",
                               widget=forms.TextInput(attrs={'placeholder': "Nom d'utilisateur"}))


class TicketCreation(forms.ModelForm):
    # Ticket creation form
    class Meta:
        # bind the form to Ticket model, use title, description and image field
        model = Ticket
        fields = ['title', 'description', 'image']

    def customSave(self, user):
        # customSave method to add the user in argument as the ticket.user
        instance_ticket = self.save(commit=False)
        instance_ticket.user = user
        instance_ticket.save()
        return instance_ticket


class ReviewCreation(forms.ModelForm):
    # Review Creation form
    # custom rating field that will be used to get Review.rating
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
        # Bind the form to Review model and use headline body and ticket field
        model = Review
        fields = ['headline', 'body', 'ticket']
        labels = {
            'headline': "Titre",
            'body': "Commentaire",
        }
        # hide the ticket field
        widgets = {
            'ticket': forms.HiddenInput(attrs={'type': 'hidden'})
        }

    def customSave(self, user, ratingcustom):
        # method to get Review.user as the user in argument and Review.rating as ratingcustom in argument
        instanceReview = self.save(commit=False)
        instanceReview.user = user
        instanceReview.rating = ratingcustom
        instanceReview.save()
        return instanceReview


class ReviewCreationWithoutTicket(forms.ModelForm):
    # Review Creation form when there isn't a previous ticket (ticket will be created alongside the review)
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
        # bind the form to Review model, use headline and body field
        model = Review
        fields = ['headline', 'body']
        labels = {
            'headline': "Titre",
            'body': "Commentaire",
        }

