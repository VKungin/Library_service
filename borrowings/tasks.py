from datetime import timedelta

from django.utils import timezone

from notifications.telegram_notifications import send_notification
from .models import Borrowing

from celery import shared_task


@shared_task
def check_overdue_borrowings():
    tomorrow = timezone.now().date() + timedelta(days=1)
    overdue_borrowings = Borrowing.objects.filter(
        expected_return_date__lte=tomorrow, actual_return_date=None
    )

    if overdue_borrowings:
        for borrowing in overdue_borrowings:
            notification_message = (
                f"The return of the book {borrowing.book.title} is overdue!"
            )
            user = borrowing.user
            if user.notifications.exists():
                send_notification(borrowing, notification_message)
    else:
        borrowings = Borrowing.objects.filter(user__is_superuser=True).first()
        send_notification(borrowings, "No borrowings overdue today!")
