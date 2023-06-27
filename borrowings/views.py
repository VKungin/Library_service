from rest_framework import generics


from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingCreateSerializer,
    BorrowingDetailSerializer,
)


class BorrowingCreateView(generics.CreateAPIView):
    queryset = Borrowing.objects.select_related()
    serializer_class = BorrowingCreateSerializer


class BorrowingDetailView(generics.RetrieveUpdateAPIView):
    queryset = Borrowing.objects.select_related()
    serializer_class = BorrowingDetailSerializer
