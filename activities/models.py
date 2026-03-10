from django.db import models
from accounts.models import User

class Activity(models.Model):

    title = models.CharField(max_length=200)

    description = models.TextField()

    location = models.CharField(max_length=200)

    start_datetime = models.DateTimeField()

    end_datetime = models.DateTimeField()

    max_volunteers = models.IntegerField()

    organiser = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_activities"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title