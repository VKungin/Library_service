from datetime import date

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingCreateSerializer,
    BorrowingDetailSerializer,
    BorrowingReturnSerializer,
    BorrowingSerializer,
)


class BorrowingListView(generics.ListAPIView):
    queryset = Borrowing.objects.select_related()
    serializer_class = BorrowingSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            queryset = Borrowing.objects.select_related()
        else:
            queryset = Borrowing.objects.filter(user=user)

        return queryset


class BorrowingCreateView(generics.CreateAPIView):
    queryset = Borrowing.objects.select_related()
    serializer_class = BorrowingCreateSerializer
    permission_classes = (IsAuthenticated,)


class BorrowingDetailView(generics.RetrieveAPIView):
    queryset = Borrowing.objects.select_related()
    serializer_class = BorrowingDetailSerializer


class BorrowingReturnView(generics.UpdateAPIView):
    queryset = Borrowing.objects.select_related()
    serializer_class = BorrowingReturnSerializer

    def perform_update(self, serializer):
        borrowing = serializer.save(actual_return_date=date.today())
        book = borrowing.book
        book.inventory += 1
        book.save()
