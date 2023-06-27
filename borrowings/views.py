from rest_framework import generics, status
from rest_framework.response import Response

from borrowings.models import Borrowing
from borrowings.serializers import BorrowingSerializer


class BorrowingCreateView(generics.CreateAPIView):
    queryset = Borrowing.objects.select_related()
    serializer_class = BorrowingSerializer

    # def create(self, request, *args, **kwargs):
    #     book_id = request.data.get("book")
    #     user_id = request.data.get("user")
    #
    #     borrowing = Borrowing.objects.create(
    #         book_id=book_id,
    #         user_id=user_id,
    #     )
    #
    #     serializer = self.get_serializer(borrowing)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
