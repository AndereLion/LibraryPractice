from rest_framework import serializers

from books.models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "author",
            "cover",
            "inventory",
            "daily_fee",
            "stripe_price_key"
        )


class BookListSerializer(BookSerializer):
    pass


class BookDetailSerializer(BookSerializer):
    pass
