from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from books.models import Book
from borrowings.models import Borrowing
from borrowings.serializers import BorrowingSerializer


class BorrowingModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='testuser@test.com', password='testpass'
        )
        self.book = Book.objects.create(title='My Book', inventory=2, daily_fee=1, author='John Doe')

    def test_valid_borrowing(self):
        borrowing = Borrowing.objects.create(
            borrow_date=timezone.now().date(),
            expected_return_date=timezone.now().date() + timedelta(days=7),
            book=self.book,
            user=self.user,
        )
        self.assertEqual(borrowing.actual_return_date, None)
        self.assertEqual(borrowing.borrow_date, timezone.now().date())
        self.assertEqual(borrowing.expected_return_date, timezone.now().date() + timedelta(days=7))
        self.assertEqual(borrowing.book, self.book)
        self.assertEqual(borrowing.user, self.user)

    def test_actual_return_date_earlier_than_today(self):
        with self.assertRaises(ValidationError):
            borrowing = Borrowing.objects.create(
                borrow_date=timezone.now().date(),
                expected_return_date=timezone.now().date() + timedelta(days=7),
                actual_return_date=timezone.now().date() - timedelta(days=1),
                book=self.book,
                user=self.user,
            )
            borrowing.full_clean()

    def test_expected_return_date_earlier_than_today(self):
        with self.assertRaises(ValidationError):
            borrowing = Borrowing.objects.create(
                borrow_date=timezone.now().date() - timedelta(days=7),
                expected_return_date=timezone.now().date() - timedelta(days=1),
                book=self.book,
                user=self.user,
            )
            borrowing.full_clean()

    def test_expected_return_date_earlier_than_borrow_date(self):
        with self.assertRaises(ValidationError):
            borrowing = Borrowing.objects.create(
                borrow_date=timezone.now().date(),
                expected_return_date=timezone.now().date() - timedelta(days=1),
                book=self.book,
                user=self.user,
            )
            borrowing.full_clean()


class TestBorrowingSerializer(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='testuser@test.com', password='testpass'
        )
        self.book = Book.objects.create(title='My Book', inventory=2, daily_fee=1, author='John Doe')

    def test_valid_borrowing_serializer(self):
        borrowing = Borrowing.objects.create(
            borrow_date=timezone.now().date(),
            expected_return_date=timezone.now().date() + timedelta(days=7),
            book=self.book,
            user=self.user,
        )
        serializer = BorrowingSerializer(borrowing)
        data = serializer.data
        self.assertEqual(data['borrow_date'], str(borrowing.borrow_date))
        self.assertEqual(data['expected_return_date'], str(borrowing.expected_return_date))
        self.assertEqual(data['actual_return_date'], borrowing.actual_return_date)
        self.assertEqual(data['book'], borrowing.book.id)
        self.assertEqual(data['user'], borrowing.user.id)

    def test_invalid_borrowing_serializer(self):
        with self.assertRaises(ValidationError):
            Borrowing.objects.create(
                borrow_date=timezone.now().date(),
                expected_return_date=timezone.now().date() - timedelta(days=7),
                book=self.book,
                user=self.user,
            )

    def test_valid_borrowing_serializer_with_actual_return_date(self):
        borrowing = Borrowing.objects.create(
            borrow_date=timezone.now().date(),
            expected_return_date=timezone.now().date() + timedelta(days=7),
            actual_return_date=timezone.now().date() + timedelta(days=5),
            book=self.book,
            user=self.user,
        )
        serializer = BorrowingSerializer(borrowing)
        data = serializer.data
        self.assertEqual(data['borrow_date'], str(borrowing.borrow_date))
        self.assertEqual(data['expected_return_date'], str(borrowing.expected_return_date))
        self.assertEqual(data['actual_return_date'], str(borrowing.actual_return_date))
        self.assertEqual(data['book'], borrowing.book.id)
        self.assertEqual(data['user'], borrowing.user.id)

    def test_valid_borrowing_serializer_with_null_actual_return_date(self):
        borrowing = Borrowing.objects.create(
            borrow_date=timezone.now().date(),
            expected_return_date=timezone.now().date() + timedelta(days=7),
            actual_return_date=None,
            book=self.book,
            user=self.user,
        )
        serializer = BorrowingSerializer(borrowing)
        data = serializer.data
        self.assertEqual(data['borrow_date'], str(borrowing.borrow_date))
        self.assertEqual(data['expected_return_date'], str(borrowing.expected_return_date))
        self.assertEqual(data['actual_return_date'], borrowing.actual_return_date)
        self.assertEqual(data['book'], borrowing.book.id)
        self.assertEqual(data['user'], borrowing.user.id)

    def test_valid_borrowing_serializer_with_null_actual_return_date_and_expected_return_date(self):
        with self.assertRaises(TypeError):
            Borrowing.objects.create(
                borrow_date=timezone.now().date(),
                expected_return_date=None,
                actual_return_date=None,
                book=self.book,
                user=self.user,
            )
