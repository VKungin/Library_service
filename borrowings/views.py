from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import (
    BorrowingCreateSerializer,
    BorrowingDetailSerializer,
    BorrowingReturnSerializer,
    BorrowingListSerializer,
)
from .models import Borrowing
from notifications.telegram_notifications import send_notification
from rest_framework.permissions import IsAuthenticated


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.select_related()
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods=["post"], url_path="return")
    def return_book(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.return_book()

        return Response(status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.action == "create":
            return BorrowingCreateSerializer
        elif self.action == "retrieve":
            return BorrowingDetailSerializer
        elif self.action == "return_book":
            return BorrowingReturnSerializer
        else:
            return BorrowingListSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            queryset = Borrowing.objects.select_related()
        else:
            queryset = Borrowing.objects.filter(user=user)

        user_id = self.request.query_params.get("user_id")
        if user_id:
            queryset = queryset.filter(user_id=user_id)

        is_active = self.request.query_params.get("is_active")
        if is_active:
            is_active = is_active.lower() == "true"
            queryset = queryset.filter(actual_return_date__isnull=is_active)

        return queryset

    def perform_create(self, serializer):
        borrowing = serializer.save()
        user = borrowing.user
        if user.notifications.exists():
            message = (
                f"New borrowing created:\n"
                f"book: {borrowing.book.title}\n"
                f"expected return date:{borrowing.expected_return_date}"
            )

            send_notification(borrowing, message)

        return borrowing
