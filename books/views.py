from rest_framework.viewsets import ModelViewSet

from books.models import Book
from books.serializers import (
    BookSerializer,
    BookListSerializer,
    BookDetailSerializer
)


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return BookListSerializer
        if self.action == "retrieve":
            return BookDetailSerializer

        return self.serializer_class
