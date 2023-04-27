from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from borrowings.models import Borrowing
from books.serializers import BookDetailSerializer

from payment import serializers as payment_serializers
from payment.models import Payment


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user"
        )
        read_only_fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user"
        )

class BorrowingListSerializer(BorrowingSerializer):

    class Meta:
        model = Borrowing
        fields = (
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        payment_serializer = payment_serializers.PaymentDetailSerializer(
            Payment.objects.filter(borrowing_id=instance.id),
            many=True,
            read_only=True
        )
        data["payments"] = payment_serializer.data
        return data


class BorrowingDetailSerializer(serializers.ModelSerializer):
    book = BookDetailSerializer()

    class Meta:
        model = Borrowing
        fields = [
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "user",
            "book"
        ]


class BorrowingCreateSerializer(BorrowingSerializer):
    class Meta:
        model = Borrowing
        fields = "__all__"
        read_only_fields = ("id", "user", "actual_return_date")

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


class BorrowingReturnSerializer(BorrowingSerializer):
    class Meta:
        model = Borrowing
        fields = ("id", "actual_return_date")
