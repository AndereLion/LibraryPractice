from rest_framework import generics

from LibraryPractice.borrowings.models import Borrowing
from LibraryPractice.borrowings.serializers import (
    BorrowingListSerializer,
    BorrowingDetailSerializer,
)


class BorrowingList(generics.ListCreateAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingListSerializer


class BorrowingDetail(generics.RetrieveUpdateAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingDetailSerializer
