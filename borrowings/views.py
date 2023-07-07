from datetime import date
from django.db import transaction

from notifications.models import Notification
from notifications.telegram_notifications import send_notification

from rest_framework import generics, exceptions
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingCreateSerializer,
    BorrowingDetailSerializer,
    BorrowingReturnSerializer,
    BorrowingListSerializer,
)


class BorrowingListCreateView(generics.ListCreateAPIView):
    queryset = Borrowing.objects.select_related()
    serializer_class = BorrowingCreateSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return BorrowingCreateSerializer
        else:
            return BorrowingListSerializer

    def get_queryset(self):
        """admin sees all borrowing, not admin only his own"""
        user = self.request.user

        if user.is_superuser:
            queryset = Borrowing.objects.select_related()
        else:
            queryset = Borrowing.objects.filter(user=user)

        """filter by user_id and is_active"""
        user_id = self.request.query_params.get("user_id")
        if user_id:
            queryset = queryset.filter(user_id=user_id)

        is_active = self.request.query_params.get("is_active")
        if is_active:
            is_active = is_active.lower() == "true"
            filtered_queryset = []
            for borrowing in queryset:
                if borrowing.is_active == is_active:
                    filtered_queryset.append(borrowing)
            queryset = filtered_queryset

        return queryset

    def perform_create(self, serializer):
        borrowing = serializer.save()
        message = (
            f"New borrowing created:\n"
            f"book: {borrowing.book.title}\n"
            f"expected return date:{borrowing.expected_return_date}"
        )

        user = borrowing.user
        if user.notifications.exists():
            send_notification(borrowing, message)

        return borrowing


class BorrowingDetailView(generics.RetrieveAPIView):
    queryset = Borrowing.objects.select_related()
    serializer_class = BorrowingDetailSerializer
    permission_classes = (IsAuthenticated,)


class BorrowingReturnView(generics.UpdateAPIView):
    queryset = Borrowing.objects.select_related()
    serializer_class = BorrowingReturnSerializer
    permission_classes = (IsAdminUser,)

    def perform_update(self, serializer):
        borrowing = serializer.instance
        if borrowing.actual_return_date:
            raise exceptions.ValidationError("The book has already been returned.")
        else:
            # with transaction.atomic():
            borrowing = serializer.save(actual_return_date=date.today())
            book = borrowing.book
            book.inventory += 1
            book.save()

            user = borrowing.user
            if user.notifications.exists():
                message = (
                    f"Borrowing returned:\n"
                    f"book: {borrowing.book.title}\n"
                    f"returned date:{borrowing.actual_return_date}"
                )

                send_notification(borrowing, message)
