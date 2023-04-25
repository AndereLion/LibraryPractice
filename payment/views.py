from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import Payment
from .serializers import PaymentListSerializer, PaymentDetailSerializer


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Payment.objects.all()
        else:
            return Payment.objects.filter(user=self.request.user)


class PaymentDetailAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Payment.objects.all()
        else:
            return Payment.objects.filter(user=self.request.user)