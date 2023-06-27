from rest_framework import generics, status
from rest_framework.response import Response

from borrowings.models import Borrowing
from borrowings.serializers import BorrowingSerializer


class BorrowingCreateView(generics.CreateAPIView):
    queryset = Borrowing.objects.select_related()
    serializer_class = BorrowingSerializer
