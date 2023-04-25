from django.core.exceptions import ValidationError
from rest_framework import serializers

from borrowings.models import Borrowing
from books.serializers import BookSerializer


class BorrowingSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "book",
            "borrowed_at",
            "expected_return_date",
            "actual_return_date",
            "is_active",
        )


class BorrowingCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "book",
            "borrowed_at",
            "expected_return_date",
            "actual_return_date"
        )
        read_only_fields = ("id", "borrowed_at", "actual_return_date")

    def create(self, validated_data):

        book = validated_data.get("book")
        if book.inventory <= 0:
            raise ValidationError(
                {"error": "No books available"}
            )

        borrowing = Borrowing.objects.create(**validated_data)
        book.inventory -= 1
        book.save()

        return borrowing


class BorrowReturnSerializer(BorrowingSerializer):
    class Meta:
        model = Borrowing
        fields = ("id", "actual_return_date")
