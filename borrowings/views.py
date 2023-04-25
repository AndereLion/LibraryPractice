from django.db import transaction
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingSerializer,
    BorrowReturnSerializer,
    BorrowingCreateSerializer
)


class BorrowingViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = BorrowingSerializer
    queryset = Borrowing.objects.select_related("book")
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        queryset = self.queryset
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

    def get_serializer_class(self):

        if self.action == "create":
            return BorrowingCreateSerializer

        if self.action == "return_borrow":
            return BorrowReturnSerializer

        return BorrowingSerializer

    def perform_create(self, serializer):

        serializer.save(user=self.request.user)

    @action(methods=["POST"], detail=True, url_path="return")
    @transaction.atomic
    def return_borrow(self, request, pk=None):

        borrow = self.get_object()
        serializer = self.get_serializer(borrow, data=request.data)

        if borrow.actual_return_date is None:

            if serializer.is_valid():

                serializer.save()
                borrow.book.inventory += 1
                borrow.book.save()

                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"message": f"User {borrow.user.email} has returned the book."},
            status=status.HTTP_400_BAD_REQUEST,
        )
