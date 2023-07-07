from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient

from books.models import Book
from borrowings.models import Borrowing
from borrowings.serializers import BorrowingCreateSerializer, BorrowingListSerializer

BORROWING_URL = reverse("borrowings:list-create")


def sample_book(**params):
    defaults = {
        "title": "Test book",
        "author": "Test author",
        "cover": "hard",
        "inventory": "10",
        "daily_fee": "2.00",
    }
    return Book.objects.create(**defaults)


def sample_borrowing(user=None, **params):
    book = sample_book()
    defaults = {
        "book": book,
        "user": user or get_user_model().objects.get(email="test@test.com"),
        "expected_return_date": "2023-07-15",
    }
    return Borrowing.objects.create(**defaults)


class UnauthenticatedBorrowingApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required_post(self):
        res = self.client.post(BORROWING_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth_required_get(self):
        res = self.client.get(BORROWING_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBorrowingApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_list_borrowing(self):
        sample_borrowing(user=self.user)
        sample_borrowing(user=self.user)

        res = self.client.get(BORROWING_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        borrowing = Borrowing.objects.all()
        serializer = BorrowingListSerializer(borrowing, many=True)
        self.assertEqual(res.data, serializer.data)

    def test_create_borrowing(self):
        book = sample_book()
        payload = {
            "book": book.id,
            "expected_return_date": "2023-07-15",
        }

        res = self.client.post(BORROWING_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_auth_required_get(self):
        res = self.client.get(BORROWING_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class AdminBorrowingApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@test.com",
            "testpass",
            is_staff=True,
        )
        self.client.force_authenticate(self.user)

    def test_create_borrowing(self):
        book = sample_book()
        payload = {
            "book": book.id,
            "expected_return_date": "2023-07-15",
        }

        res = self.client.post(BORROWING_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
