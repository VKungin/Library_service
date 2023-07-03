from django.db import models

from users.models import User


class Notification(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )
    chat_id = models.CharField(max_length=255, null=True)
