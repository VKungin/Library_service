from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover_choices = [("hard", "Hard"), ("soft", "Soft")]
    cover = models.CharField(max_length=4, choices=cover_choices)
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.title}, inventory: {self.inventory}"
