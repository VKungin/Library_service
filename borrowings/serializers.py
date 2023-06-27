from rest_framework import serializers

from books.models import Book
from borrowings.models import Borrowing
from users.models import User


class BorrowingSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "book",
            "user",
            "expected_return_date",
            "actual_return_date",
        )

    def create(self, validated_data):
        book = validated_data["book"]

        if book.inventory == 0:
            raise serializers.ValidationError(
                "Inventory is zero for the selected book."
            )

        book.inventory -= 1
        book.save()

        borrowing = Borrowing.objects.create(**validated_data)
        return borrowing
