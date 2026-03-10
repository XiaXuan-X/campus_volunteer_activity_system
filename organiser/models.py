from django.db import models
from accounts.models import User
from activities.models import Activity


class Application(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    volunteer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="applications"
    )

    activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE,
        related_name="applications"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    applied_at = models.DateTimeField(auto_now_add=True)

    attended = models.BooleanField(default=False)

    class Meta:
        unique_together = ('volunteer', 'activity')

    def __str__(self):
        return f"{self.volunteer} - {self.activity}"