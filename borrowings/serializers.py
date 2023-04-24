from rest_framework import serializers

from borrowings.models import Borrowing
from book.serializers import BookDetailSerializer
from django.core.exceptions import ValidationError


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user"
        )


class BorrowingListSerializer(BorrowingSerializer):
    book = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="title"
    )
    user = serializers.SlugRelatedField(
        read_only=True, slug_field="email"
    )

    class Meta:
        model = Borrowing
        fields = (
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user"
        )


class BorrowingDetailSerializer(serializers.ModelSerializer):
    book = BookDetailSerializer()

    class Meta:
        model = Borrowing
        fields = ["id",
                  "borrow_date",
                  "expected_return_date",
                  "actual_return_date",
                  "user",
                  "book"]


class BorrowingCreateSerializer(BorrowingSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Borrowing
        fields = ["id", "borrow_date", "expected_return_date", "actual_return_date", "user", "book"]

    def validate_book(self, book):
        if book.inventory == 0:
            raise ValidationError("The book inventory is 0.")
        return book

    def create(self, validated_data):
        book = validated_data["book"]
        book.inventory -= 1
        book.save()
        borrowing = Borrowing.objects.create(**validated_data)
        return borrowing
