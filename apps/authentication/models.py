from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # We use Email for login, so we make it unique
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, blank=True)

    # This matches the "Verification" state in your UI
    is_email_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username'] # Django still needs this for internal tools



    def __str__(self):
        return self.email
