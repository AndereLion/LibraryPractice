from django.utils import timezone

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from LibraryPractice.borrowings.models import Borrowing
from LibraryPractice.borrowings.serializers import (
    BorrowingListSerializer,
    BorrowingDetailSerializer,
)


class BorrowingList(generics.ListCreateAPIView):
    serializer_class = BorrowingListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        is_active = self.request.query_params.get("is_active")
        if is_active == "true":
            return Borrowing.objects.filter(
                actual_return_date__isnull=True, expected_return_date__lte=timezone.now()
            )
        elif self.request.user.is_staff:
            user_id = self.request.query_params.get("user_id")
            if user_id:
                return Borrowing.objects.select_related("book", "user").filter(user_id=user_id)
            return Borrowing.objects.select_related("book", "user").all()
        return Borrowing.objects.select_related("book", "user").filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BorrowingDetail(generics.RetrieveUpdateAPIView):
    serializer_class = BorrowingDetailSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Borrowing.objects.select_related("book", "user")
        else:
            return Borrowing.objects.select_related(
                "book", "user"
            ).filter(user=self.request.user)
