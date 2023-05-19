from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # User class, disabled first/last name because they won't be needed
    first_name = None
    last_name = None
