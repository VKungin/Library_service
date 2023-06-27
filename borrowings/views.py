from datetime import date

from rest_framework import generics


from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingCreateSerializer,
    BorrowingDetailSerializer,
    BorrowingReturnSerializer,
)


class BorrowingCreateView(generics.CreateAPIView):
    queryset = Borrowing.objects.select_related()
    serializer_class = BorrowingCreateSerializer


class BorrowingDetailView(generics.RetrieveAPIView):
    queryset = Borrowing.objects.select_related()
    serializer_class = BorrowingDetailSerializer


class BorrowingReturnView(generics.UpdateAPIView):
    queryset = Borrowing.objects.select_related()
    serializer_class = BorrowingReturnSerializer

    def perform_update(self, serializer):
        serializer.save(actual_return_date=date.today())
