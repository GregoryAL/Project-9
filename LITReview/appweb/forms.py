from django import forms
from appweb.models import UserFollows, Ticket, Review
from django.shortcuts import get_object_or_404
from authentication.models import User



class FollowingForm(forms.Form):
    username = forms.CharField(max_length=128, label="Suivre d'autres utilisateurs", widget=forms.TextInput(attrs={'placeholder': "Nom d'utilisateur"}))

    #class Meta:
        #model = UserFollows
        #fields = ['username']

        #widgets = {
            #'followed_user': forms.TextInput(attrs={'placeholder': "Nom d'utilisateur"})
        #}
        #labels = {
            #'followed_user': "Suivre d'autres utilisateurs"
        #}

    #def clean(self):
        #cleaned_data = super(forms.ModelForm, self).clean()
        #self.instance.followed_user = get_object_or_404(User, username=cleaned_data['followed_user'])
        #followed_user = self.cleaned_data['followed_user']
        #self.cleaned_data['followed_user'] = get_object_or_404(User, username=followed_user)
        #return cleaned_data


class TicketCreation(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description']


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
            'ticket': forms.HiddenInput()
        }
