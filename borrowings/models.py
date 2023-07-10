import datetime
import decimal

from django.db import models

from books.models import Book
from users.models import User


class Borrowing(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="borrowings")
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)

    @property
    def is_active(self) -> bool:
        return not bool(self.actual_return_date)

    def get_type(self) -> str:
        if self.expected_return_date < datetime.date.today():
            return "fine"
        return "payment"

    def get_money_to_pay(self) -> decimal:
        days_borrowed = (self.expected_return_date - self.borrow_date).days
        money_to_pay = self.book.daily_fee * days_borrowed

        payment_type = self.get_type()
        if payment_type == "fine":
            money_to_pay *= 2

        return money_to_pay

    def __str__(self):
        return f"id: {self.id}, book: {self.book.title}"
