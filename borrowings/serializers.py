from rest_framework import serializers

from books.models import Book
from borrowings.models import Borrowing
from users.models import User


class BorrowingSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "book",
            "user",
            "expected_return_date",
            "actual_return_date",
        )
