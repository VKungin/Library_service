from django.db import models

from borrowings.models import Borrowing


class Payment(models.Model):
    status_choices = [
        ("pending", "PENDING"),
        ("paid", "PAID"),
        ("canceled", "CANCELED"),
    ]
    status = models.CharField(max_length=8, choices=status_choices, default="PENDING")
    type_choices = [("payment", "PAYMENT"), ("fine", "FINE")]
    type = models.CharField(max_length=7, choices=type_choices, default="PAYMENT")
    borrowing = models.OneToOneField(
        Borrowing, on_delete=models.CASCADE, related_name="payments"
    )
    session_url = models.URLField()
    session_id = models.CharField(max_length=64)
    money_to_pay = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.id} {self.status}"
