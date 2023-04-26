from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from appweb.forms import TicketCreation, FollowingForm, ReviewCreation
from authentication.models import User

from appweb.models import Ticket, Review, UserFollows


@login_required
def home(request):
    usersfollowed = UserFollows.objects.filter(followed_user=request.user.id)
    ticketsToDisplay = []
    ticketsToDisplay += Ticket.objects.filter(user=request.user.id)
    for userfollowed in usersfollowed:
        ticketsToDisplay += Ticket.objects.filter(user=userfollowed.id)
    return render(request, 'appweb/home.html', {'tickets': ticketsToDisplay})

@login_required
def subscription(request):
    if request.method == "GET":
        form = FollowingForm()
        return render(request, 'appweb/subscription.html', {'form': form})
    elif request.method == "POST":
        form = FollowingForm(request.POST)
        userentered = form.cleaned_data.get("followed_user")
        form.followed_user = get_object_or_404(User, username=userentered)
        if form.is_valid():
            subscription_object = form.save(commit=False)
            #userEntered = subscription_object.cleaned_data['followed_user']
            #userToFollow = User.objects.get(username=userEntered)
            #subscription_object.followed_user = userToFollow
            subscription_object.following = request.user
            subscription_object.save()
            return redirect('home')
    #if request.method == 'POST':
        #form = subscriptions(request.POST)
        #if form.is_valid():
            #userEntered = form.cleaned_data['followed_user']

            #userToFollow = User.objects.get(username=userEntered).id
            #userFollowing = request.user.id
            #form.save()


@login_required
def ticket_creation(request, id_ticket=None):
    instance_ticket = Ticket.objects.get(pk=id_ticket) if id_ticket is not None else None
    if request.method == "GET":
        form = TicketCreation(instance=instance_ticket)
        return render(request, 'appweb/ticketcreation.html', {'form': form})
    elif request.method == "POST":
        form = TicketCreation(request.POST, instance=instance_ticket)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('home')


@login_required
def review_creation(request, id_ticket=None, id_review=None):
    instance_review = Review.object.get(pk=id_review) if id_review is not None else None
    instance_ticket = Ticket.object.get(pk=id_ticket) if id_ticket is not None else None
    if request.method == "GET":
        form = ReviewCreation(instance=instance_review)
        form.ticket = instance_ticket
        return render(request, 'appweb/reviewcreation.html', {'form': form})
    elif request.method == "POST":
        form = ReviewCreation(request.POST, instance=instance_review)
        review = form.save(commit=False)
        review.user = request.user
        review.save()
        return redirect('home')


@login_required()
def display_ticket(request):
    usersfollowed = list(UserFollows.objects.filter(followed_user=request.user.id))
    ticketsToDisplay = []
    for userfollowed in usersfollowed:
        ticketsToDisplay += Ticket.objects.filter(user=userfollowed.id)
    return render(request, 'appweb/home.html', {'tickets': ticketsToDisplay})




