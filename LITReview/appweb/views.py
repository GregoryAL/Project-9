from itertools import chain

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
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
        Q(user__followed_by__user=request.user) |
        Q(review__user=request.user)
    ).distinct().annotate(content_type=Value('TicketWithReview', CharField())).exclude(Q(review=None))
    ticketsAndReviews = sorted(chain(ticketsWithoutReview, reviews), key=lambda x: x.time_created, reverse=True)
    return render(request, 'appweb/home.html', {'posts': ticketsAndReviews, 'ticketswithreview': ticketsWithReview})


@login_required
def posts(request):
    reviews = Review.objects.filter(
        Q(user=request.user)
    ).annotate(content_type=Value('Review', CharField()))
    tickets = Ticket.objects.filter(
        Q(user=request.user)
    ).distinct().annotate(content_type=Value('Ticket', CharField()))
    reviewsTicket = Ticket.objects.filter(
        Q(review__user=request.user)
    ).distinct().annotate(content_type=Value('ReviewsTicket', CharField()))
    ticketsAndReviews = sorted(chain(tickets, reviews), key=lambda x: x.time_created, reverse=True)
    return render(request, 'appweb/posts.html', {'posts': ticketsAndReviews, 'reviewsticket': reviewsTicket})


@login_required
def subscription(request):
    usersfollowing = UserFollows.objects.filter(user=request.user.id)
    usersfollowed = UserFollows.objects.filter(followed_user=request.user.id)
    errormessages = {
        'donotexist': "L'utilisateur n'existe pas.",
        'autosubscribed': "Vous ne pouvez pas vous abonnez à vous même.",
        'alreadysubscrided': "Vous êtes déjà abonné(e) à cet utilisateur."
    }
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
            try:
                followed_user = User.objects.get(username=username)
            except ObjectDoesNotExist:
                message = "L'utilisateur n'existe pas."
            else:
                if followed_user == request.user:
                    message = "Vous ne pouvez pas vous abonnez à vous même."
                else:
                    try:
                        subscript = UserFollows.objects.create(followed_user=followed_user, user=request.user)
                    except IntegrityError:
                        message = "Vous êtes déjà abonné(e) à cet utilisateur."
                    else:
                        subscript.save()
                        message = "Vous vous êtes bien abonné à " + str(followed_user.username) + "."
                    finally:
                        pass
            finally:
                context = {
                    'form': FollowingForm(),
                    'usersfollowing': usersfollowing,
                    'usersfollowed': usersfollowed,
                    'message': message
                }
                return render(request, 'appweb/subscription.html', context=context)


@login_required
def deletesubscription(request, id_subscription):
    if request.method == 'GET':
        usersfollowing = get_object_or_404(UserFollows, pk=id_subscription)
        if usersfollowing.user == request.user:
            usersfollowing.delete()
            return redirect('subscription')
        else:
            return redirect('home')

@login_required
def deletereview(request, id_review):
    if request.method == 'GET':
        reviewToDelete = get_object_or_404(Review, pk=id_review)
        if reviewToDelete.user == request.user:
            reviewToDelete.delete()
            return redirect('posts')

@login_required
def deleteticket(request, id_ticket):
    if request.method == 'GET':
        ticketToDelete = get_object_or_404(Ticket, pk=id_ticket)
        if ticketToDelete.user == request.user:
            ticketToDelete.delete()
            return redirect('posts')


@login_required
def ticket_creation(request, id_ticket=None):
    instance_ticket = Ticket.objects.get(pk=id_ticket) if id_ticket is not None else None
    if id_ticket is not None and instance_ticket.user.id != request.user.id:
        return redirect('home')
    else:
        if request.method == "GET":
            form = TicketCreation(instance=instance_ticket)
            return render(request, 'appweb/ticketcreation.html', {'form': form})
        elif request.method == "POST":
            form = TicketCreation(request.POST, request.FILES, instance=instance_ticket)
            if form.is_valid():
                instance_ticket = form.customSave(request.user)
                return redirect('home')


@login_required
def review_modification(request, id_review):
    instance_review = Review.objects.get(pk=id_review)
    instance_ticket = Ticket.objects.get(pk=instance_review.ticket.id)
    if instance_review.user.id == request.user.id:
        if request.method == "GET":
            form = ReviewCreation(instance=instance_review, initial={'ratingcustom': instance_review.rating})
            context = {
                'form': form,
                'instance_ticket': instance_ticket
                }
            return render(request, 'appweb/reviewmodification.html', context=context)
        elif request.method == "POST":
            form = ReviewCreation(request.POST, instance=instance_review)
            if form.is_valid():
                rating = form.cleaned_data['ratingcustom']
                review = form.customSave(request.user, rating)
                return redirect('home')
    else:
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
            rating = form.cleaned_data['ratingcustom']
            review = form.customSave(request.user, rating)
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
        ticket_form = TicketCreation(request.POST, request.FILES)
        review_form = ReviewCreationWithoutTicket(request.POST)
        if ticket_form.is_valid():
            instance_ticket = ticket_form.customSave(request.user)
            if review_form.is_valid():
                ratingcustom = review_form.cleaned_data['ratingcustom']
                instance_review = review_form.save(commit=False)
                instance_review.user = request.user
                instance_review.rating = ratingcustom
                instance_review.ticket = instance_ticket
                instance_review.save()
                return redirect('home')
