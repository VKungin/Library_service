from datetime import date

from datetime import date
from rest_framework import exceptions
from rest_framework import serializers

from books.models import Book
from books.serializers import BookSerializer
from borrowings.models import Borrowing
from users.serializers import UserSerializer
from notifications.telegram_notifications import send_notification


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "book",
            "user",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "is_active",
        )


class BorrowingListSerializer(BorrowingSerializer):
    book = serializers.StringRelatedField()

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "book",
            "user",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "is_active",
        )


class BorrowingCreateSerializer(BorrowingSerializer):
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


class BorrowingDetailSerializer(BorrowingSerializer):
    book = BookSerializer()
    user = UserSerializer()

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "book",
            "user",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "is_active",
        )


class BorrowingReturnSerializer(BorrowingSerializer):
    class Meta:
        model = Borrowing
        fields = ("actual_return_date",)

    def return_book(self):
        borrowing = self.instance

        if borrowing.actual_return_date:
            raise exceptions.ValidationError("The book has already been returned.")
        else:
            borrowing.actual_return_date = date.today()
            borrowing.save()

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

        return borrowing
