from django.urls import path
from .views import PaymentListAPIView, PaymentDetailAPIView

urlpatterns = [
    path('payments/', PaymentListAPIView.as_view(), name='payment_list'),
    path('payments/<int:pk>/', PaymentDetailAPIView.as_view(), name='payment_detail'),
]

app_name = "payment"
