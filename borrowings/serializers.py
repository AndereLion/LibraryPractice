from rest_framework import serializers

from borrowing.models import Borrowing
from book.serializers import BookDetailSerializer


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

