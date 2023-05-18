from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth import login, authenticate, logout
from django.conf import settings


def login_page(request):
    # View that manage user login using login form, and redirect the user to home if login succeed
    form = forms.LoginForm()
    message = ''
    # for POST method :
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            # If info typed by user are valid , then we try to authenticate with login/password entered
            # If it works, authenticate stock in a variable the object user related to login/password, it not None is
            # stocked in that variable
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                # If authenticated worked, the user is logged in and redirected to home
                login(request, user)
                return redirect('home')
            else:
                # if not, a message is displayed to inform the user than login/password are invalid
                message = 'Identifiants invalides.'
    # for GET method:
    return render(
        request, 'authentication/login.html', context={'form': form, 'message': message})


def logout_user(request):
    # logout the user then redirect to log in template
    logout(request)
    return redirect('login')


def signup_page(request):
    # View that manage user sign-up
    form = forms.SignupForm()
    # for POST method:
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            # when info type by user are valid, user is created in the User table then the user is logged in and
            # redirected to 'home' which has been set up as login_redirect_url in the settings.py file
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    # for GET method
    return render(request, 'authentication/signup.html', context={'form': form})
