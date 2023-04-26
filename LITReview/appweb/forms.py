from django import forms
from appweb.models import UserFollows, Ticket, Review
from django.shortcuts import get_object_or_404
from authentication.models import User



class FollowingForm(forms.ModelForm):
    class Meta:
        model = UserFollows
        fields = ['followed_user']
        widgets = {
            'followed_user': forms.TextInput(attrs={'placeholder': "Nom d'utilisateur"})
        }
        labels = {
            'followed_user': "Suivre d'autres utilisateurs"
        }

    #def clean_followed_user(self):
        #userentered = self.cleaned_data.get("followed_user")
        #user = get_object_or_404(User, username=userentered)
        #return user


class TicketCreation(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description']



class ReviewCreation(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']
        labels = {
            'headline': "Titre",
            'rating': "Note",
            'body': "Commentaire"
        }
