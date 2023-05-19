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
    # view used for home template
    # query to store all the reviews written by logged-in user or by users followed by logged-in user
    # add a content type with a "Review" value
    reviews = Review.objects.filter(
        Q(user=request.user) |
        Q(user__followed_by__user=request.user)
    ).distinct().annotate(content_type=Value('Review', CharField()))
    # query to store all the tickets written by logged-in user or by users followed by logged-in user which doesn't
    # have a review, add a content type with a "TicketWithoutReview" value
    ticketsWithoutReview = Ticket.objects.filter(
        Q(user=request.user) |
        Q(user__followed_by__user=request.user)
    ).distinct().annotate(content_type=Value('TicketWithoutReview', CharField())).exclude(~Q(review=None))
    # query to store all the tickets written by logged-in user or by users followed by logged-in user which have a
    # review, add a content type with a "TicketWithReview" value
    ticketsWithReview = Ticket.objects.filter(
        Q(user=request.user) |
        Q(user__followed_by__user=request.user) |
        Q(review__user=request.user)
    ).distinct().annotate(content_type=Value('TicketWithReview', CharField())).exclude(Q(review=None))
    # create a variable sorting tickets without review and review by time created
    ticketsAndReviews = sorted(chain(ticketsWithoutReview, reviews), key=lambda x: x.time_created, reverse=True)
    # return the sorted variable plus the ticketwithreview variable which will be used to display alongside the review
    # (as a review can't exist without ticket)
    return render(request, 'appweb/home.html', {'posts': ticketsAndReviews, 'ticketswithreview': ticketsWithReview})


@login_required
def posts(request):
    # view used for posts template
    # query to store all the review written by logged-in user, add a 'review' content type
    reviews = Review.objects.filter(
        Q(user=request.user)
    ).annotate(content_type=Value('Review', CharField()))
    # query to store all the tickets written by logged-in user and add a 'ticket' content type
    tickets = Ticket.objects.filter(
        Q(user=request.user)
    ).distinct().annotate(content_type=Value('Ticket', CharField()))
    # query to store all the tickets when the review has been written by logged-in user. Add a ReviewsTicket content
    # type
    reviewsTicket = Ticket.objects.filter(
        Q(review__user=request.user)
    ).distinct().annotate(content_type=Value('ReviewsTicket', CharField()))
    # chain tickets and review and sort them by time created
    ticketsAndReviews = sorted(chain(tickets, reviews), key=lambda x: x.time_created, reverse=True)
    # return both the ticketsAndReviews and reviewsTicket variable
    return render(request, 'appweb/posts.html', {'posts': ticketsAndReviews, 'reviewsticket': reviewsTicket})


@login_required
def subscription(request):
    # view used for to subscribe to a user
    # query to get the users followed by logged-in user
    usersfollowing = UserFollows.objects.filter(user=request.user.id)
    # query to get users that follows logged-in user
    usersfollowed = UserFollows.objects.filter(followed_user=request.user.id)
    # GET method :
    if request.method == "GET":
        # bind to FollowingForm form
        form = FollowingForm()
        # add form usersfollowing and usersfollowed to context
        context = {
            'form': form,
            'usersfollowing': usersfollowing,
            'usersfollowed': usersfollowed
        }
        return render(request, 'appweb/subscription.html', context=context)
    # POST method
    elif request.method == "POST":
        # add the context form POST info to the form
        form = FollowingForm(request.POST)
        # check form validity
        if form.is_valid():
            # get the typed in username from form
            username = form.cleaned_data['username']
            try:
                # check if user exist and store the object user if so
                followed_user = User.objects.get(username=username)
            except ObjectDoesNotExist:
                # raise an error if user doesn't exist and add a message to message variable
                message = "L'utilisateur n'existe pas."
            else:
                # check if the user typed in is the same as the user logged-in and raise an exception if so
                if followed_user == request.user:
                    message = "Vous ne pouvez pas vous abonnez à vous même."
                else:
                    # check if the user typed in is already followed by user logged-in (through model unique_together
                    # meta) by creating the object subscription
                    try:
                        subscript = UserFollows.objects.create(followed_user=followed_user, user=request.user)
                    except IntegrityError:
                        message = "Vous êtes déjà abonné(e) à cet utilisateur."
                    else:
                        # save the subscription object to the UserFollows table and store a successful message
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
    # delete subscription view
    if request.method == 'GET':
        # query to get the object subscription from id_subscription
        usersfollowing = get_object_or_404(UserFollows, pk=id_subscription)
        # check if the user following is the logged-in user
        # if so, delete the subscription and return to subscription page
        # if not, go to home page
        if usersfollowing.user == request.user:
            usersfollowing.delete()
            return redirect('subscription')
        else:
            return redirect('home')


@login_required
def deletereview(request, id_review):
    # view used to delete a review
    if request.method == 'GET':
        # query to get the object review from id_review
        reviewToDelete = get_object_or_404(Review, pk=id_review)
        # check if the review's writer is the logged-in user
        # if so, delete the review and return to posts page
        # if not, go to home page
        if reviewToDelete.user == request.user:
            reviewToDelete.delete()
            return redirect('posts')
        else:
            return redirect('home')


@login_required
def deleteticket(request, id_ticket):
    # view used to delete a ticket
    if request.method == 'GET':
        # query to get the object ticket from id_ticket
        ticketToDelete = get_object_or_404(Ticket, pk=id_ticket)
        # check if the ticket's writer is the logged-in user
        # if so, delete the ticket and return to posts page
        # if not, go to home page
        if ticketToDelete.user == request.user:
            ticketToDelete.delete()
            return redirect('posts')
        else:
            return redirect('home')


@login_required
def ticket_creation(request, id_ticket=None):
    # ticket creation/modification view
    # query to get the ticket in argument if it's not none
    instance_ticket = Ticket.objects.get(pk=id_ticket) if id_ticket is not None else None
    # check if the ticket's writer is the logged-in user if it's a modification
    # if not redirect to home
    if id_ticket is not None and instance_ticket.user.id != request.user.id:
        return redirect('home')
    else:
        # get method use the ticketcreation form, will be used as a modification is there s an object ticket
        if request.method == "GET":
            form = TicketCreation(instance=instance_ticket)
            return render(request, 'appweb/ticketcreation.html', {'form': form})
        # post method get the form in context, including image if there's one
        elif request.method == "POST":
            form = TicketCreation(request.POST, request.FILES, instance=instance_ticket)
            # if form is valid save the ticket and return home
            if form.is_valid():
                instance_ticket = form.customSave(request.user)
                return redirect('home')


@login_required
def review_modification(request, id_review):
    # view used to modify a review
    # query to get the object review from id_review
    instance_review = Review.objects.get(pk=id_review)
    # query to get the object ticket from the review's related ticket
    instance_ticket = Ticket.objects.get(pk=instance_review.ticket.id)
    # check if the user that want to modify the review is the writer
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
                form.customSave(request.user, rating)
                return redirect('home')
    else:
        return redirect('home')


@login_required
def review_creation(request, id_ticket=None):
    # view used to create a review
    # query to get the ticket associated to the review
    instance_ticket = Ticket.objects.get(pk=id_ticket) if id_ticket is not None else None
    if request.method == "GET":
        # load the form with the instance.ticket initialed as the ticket previously queried
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
            form.customSave(request.user, rating)
            return redirect('home')


@login_required
def ticket_review_creation(request):
    # view used to create a ticket and a review at the same time
    if request.method == "GET":
        # load both ticket and review forms
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
            # first check if the ticket form is valid, and if so, save the object in the table and store it in
            # instance_ticket variable
            instance_ticket = ticket_form.customSave(request.user)
            if review_form.is_valid():
                # then, save the review object in the review table once user, rating and ticket have been added
                ratingcustom = review_form.cleaned_data['ratingcustom']
                instance_review = review_form.save(commit=False)
                instance_review.user = request.user
                instance_review.rating = ratingcustom
                instance_review.ticket = instance_ticket
                instance_review.save()
                return redirect('home')
