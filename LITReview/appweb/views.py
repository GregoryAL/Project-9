from itertools import chain
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from appweb.forms import TicketCreation, FollowingForm, ReviewCreation, ReviewCreationWithoutTicket
from authentication.models import User
from appweb.models import Ticket, Review, UserFollows
from django.db.models import CharField, Value, Q



@login_required
def home(request):
    reviews = Review.objects.filter(
        Q(user=request.user) |
        Q(user__followed_by__user=request.user)
    ).annotate(content_type=Value('Review', CharField()))

    ticketsWithoutReview = Ticket.objects.filter(
        Q(user=request.user) |
        Q(user__followed_by__user=request.user)
    ).distinct().annotate(content_type=Value('TicketWithoutReview', CharField())).exclude(~Q(review=None))
    ticketsWithReview = Ticket.objects.filter(
        Q(user=request.user) |
        Q(user__followed_by__user=request.user)
    ).distinct().annotate(content_type=Value('TicketWithReview', CharField())).exclude(Q(review=None))
    ticketsAndReviews = sorted(chain(ticketsWithoutReview, ticketsWithReview, reviews), key=lambda x: x.time_created, reverse=True)
    return render(request, 'appweb/home.html', {'posts': ticketsAndReviews})


@login_required
def subscription(request):
    usersfollowing = UserFollows.objects.filter(user=request.user.id)
    usersfollowed = UserFollows.objects.filter(followed_user=request.user.id)
    if request.method == "GET":
        form = FollowingForm()
        context = {
            'form': form,
            'usersfollowing': usersfollowing,
            'usersfollowed': usersfollowed
        }
        return render(request, 'appweb/subscription.html', context=context)
    elif request.method == "POST":
        form = FollowingForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            followed_user = get_object_or_404(User, username=username)
            subscript = UserFollows.objects.create(followed_user=followed_user, user=request.user)
            subscript.save()
            return redirect('home')


@login_required
def deletesubscription(request, id_subscription):
    if request.method == 'GET':
        usersfollowing = get_object_or_404(UserFollows, pk=id_subscription)
        usersfollowing.delete()
        return redirect('subscription')

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
def review_creation(request, id_ticket=None):
    instance_ticket = Ticket.objects.get(pk=id_ticket) if id_ticket is not None else None
    if request.method == "GET":
        form = ReviewCreation(initial={'ticket': instance_ticket})
        context = {
            'form': form,
            'instance_ticket': instance_ticket,
            'id_ticket': id_ticket
            }
        return render(request, 'appweb/reviewcreation.html', context=context)
    elif request.method == "POST":
        form = ReviewCreation(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('home')


@login_required
def ticket_review_creation(request):
    if request.method == "GET":
        ticket_form = TicketCreation()
        review_form = ReviewCreationWithoutTicket()
        context = {
            'ticket_form': ticket_form,
            'review_form': review_form
            }
        return render(request, 'appweb/ticketreviewcreation.html', context=context)
    elif request.method == "POST":
        ticket_form = TicketCreation(request.POST)
        review_form = ReviewCreationWithoutTicket(request.POST)
        if ticket_form.is_valid():
            instance_ticket = ticket_form.customSave(request.user)
            if review_form.is_valid():
                instance_review = review_form.save(commit=False)
                instance_review.user = request.user
                instance_review.ticket = instance_ticket
                instance_review.save()
                return redirect('home')
