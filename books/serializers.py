from rest_framework import serializers

from books.models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "title", "author", "cover_choice", "inventory", "daily_fee")


class BookListSerializer(BookSerializer):
    pass


class BookDetailSerializer(BookSerializer):
    pass
