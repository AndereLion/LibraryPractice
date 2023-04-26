from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from books.models import Book
from books.serializers import BookSerializer

BOOK_URL = reverse("book:book-list")


def sample_book(**params):
    defaults = {
        "title": "sample book",
        "author": "sample author",
        "cover": "SOFT",
        "inventory": 10,
        "daily_fee": 1.5
    }
    defaults.update(params)
    return Book.objects.create(**defaults)


class TestBookModel(TestCase):
    def test_book_str(self):
        book = Book.objects.create(
            title="sample title",
            author="sample author",
            cover="SOFT",
            inventory=10,
            daily_fee=10.23
        )
        self.assertEqual(str(book), book.title)


class TestBookSerializer(TestCase):
    def test_book_serializer(self):
        payload = {
            "title": "test title",
            "author": "test author",
            "cover": "HARD",
            "inventory": 10,
            "daily_fee": "4.31"
        }
        serializer = BookSerializer(data=payload)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data, payload)


class TestUnauthenticatedBookApi(TestCase):
    def setUp(self) -> None:
        self.client = self.client_class()

    def test_retrieve_books_unauthorized(self):
        sample_book()
        res = self.client.get(BOOK_URL)
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_book_unauthorized(self):
        payload = {
            "title": "test title",
            "author": "test author",
            "cover": "HARD",
            "inventory": 10,
            "daily_fee": 1.5
        }
        res = self.client.post(BOOK_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_book_unauthorized(self):
        book = sample_book()
        payload = {
            "title": "updated title",
            "author": "updated author",
            "cover": "HARD",
            "inventory": 10,
            "daily_fee": 1.5
        }
        url = reverse("book:book-detail", args=[book.id])
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_book_unauthorized(self):
        book = sample_book()
        url = reverse("book:book-detail", args=[book.id])
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class TestAuthenticatedBookApi(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "test@test.com",
            "somepassword12345",
        )
        self.client.force_authenticate(self.user)

    def test_create_book(self):
        payload = {
            "title": "test title",
            "author": "test author",
            "cover": "HARD",
            "inventory": 10,
            "daily_fee": 1.5
        }
        res = self.client.post(BOOK_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        exists = Book.objects.filter(
            title=payload["title"]
        ).exists()
        self.assertTrue(exists)

    def test_create_book_invalid(self):
        payload = {
            "title": "",
            "author": "",
            "cover": "",
            "inventory": -1,
            "daily_fee": -1
        }
        res = self.client.post(BOOK_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_book(self):
        book = sample_book()
        url = reverse("book:book-detail", args=[book.id])
        res = self.client.get(url)
        serializer = BookSerializer(book)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_update_book(self):
        book = sample_book()
        payload = {
            "title": "updated title",
            "author": "updated author",
            "cover": "HARD",
            "inventory": 10,
            "daily_fee": 1.5
        }
        url = reverse("book:book-detail", args=[book.id])
        res = self.client.patch(url, payload)
        book.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(book.title, payload["title"])
        self.assertEqual(book.author, payload["author"])
        self.assertEqual(book.cover, payload["cover"])
        self.assertEqual(book.inventory, payload["inventory"])
        self.assertEqual(book.daily_fee, payload["daily_fee"])

    def test_delete_book(self):
        book = sample_book()
        url = reverse("book:book-detail", args=[book.id])
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        exists = Book.objects.filter(
            title=book.title
        ).exists()
        self.assertFalse(exists)
