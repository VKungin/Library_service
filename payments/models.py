from django.db import models

from borrowings.models import Borrowing


class Payment(models.Model):
    status_choices = [("pending", "PENDING"), ("paid", "PAID")]
    status = models.CharField(max_length=7, choices=status_choices)
    type_choices = [("payment", "PAYMENT"), ("fine", "FINE")]
    type = models.CharField(max_length=7, choices=type_choices)
    borrowing = models.OneToOneField(
        Borrowing, on_delete=models.CASCADE, related_name="payments"
    )
    session_url = models.URLField()
    session_id = models.CharField(max_length=64)
    money_to_pay = models.DecimalField(max_digits=6, decimal_places=2)
