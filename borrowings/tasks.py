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

    for borrowing in overdue_borrowings:
        notification_message = (
            f"The return of the book {borrowing.book.title} is overdue!"
        )
        send_notification(borrowing, notification_message)


#
# @shared_task
# def mul(x, y):
#     return x * y
#
#
# @shared_task
# def xsum(numbers):
#     return sum(numbers)
#
#
# @shared_task
# def count_widgets():
#     return Widget.objects.count()
#
#
# @shared_task
# def rename_widget(widget_id, name):
#     w = Widget.objects.get(id=widget_id)
#     w.name = name
#     w.save()
