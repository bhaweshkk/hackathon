from django.db import models
from django.contrib.auth.models import User


class ParticipationRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participation_records')
    event_type = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.event_type}"
