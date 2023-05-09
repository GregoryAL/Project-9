"""
URL configuration for LITReview project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import authentication.views
import appweb.views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', authentication.views.login_page, name='login'),
    path('logout/', authentication.views.logout_user, name='logout'),
    path('home/', appweb.views.home, name='home'),
    path('signup/', authentication.views.signup_page, name='signup'),
    path('subscription/', appweb.views.subscription, name='subscription'),
    path('deletesubscription/<int:id_subscription>', appweb.views.deletesubscription, name='deletesubscription'),
    path('ticketcreation/', appweb.views.ticket_creation, name='ticketcreation'),
    path('ticketcreation/<int:id_ticket>', appweb.views.ticket_creation, name='ticketcreation'),
    path('reviewcreation/', appweb.views.review_creation, name='reviewcreation'),
    path('reviewcreation/<int:id_ticket>', appweb.views.review_creation, name='reviewcreation'),
    path('reviewmodification/<int:id_review>', appweb.views.review_modification, name='reviewmodification'),
    path('ticketreviewcreation/', appweb.views.ticket_review_creation, name='ticketreviewcreation'),
    path('posts/', appweb.views.posts, name='posts')
]

