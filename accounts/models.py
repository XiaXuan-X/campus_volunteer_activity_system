from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    ROLE_CHOICES = (
        ('volunteer', 'Volunteer'),
        ('organiser', 'Organiser'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='volunteer'
    )

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    def __str__(self):
        return self.username
