from django.db import models
from django.urls import reverse
from enum import Enum


class PaymentStatus(Enum):
    PENDING = "Pending"
    PAID = "Paid"


class PaymentType(Enum):
    PAYMENT = "Payment"
    FINE = "Fine"


class Payment(models.Model):
    status = models.CharField(
        max_length=50,
        choices=[(tag, tag.value) for tag in PaymentStatus]
    )
    type = models.CharField(
        max_length=50, choices=[(tag, tag.value) for tag in PaymentType]
    )
    borrowing_id = models.PositiveIntegerField()
    session_url = models.URLField()
    session_id = models.CharField(max_length=100)
    money_to_pay = models.DecimalField(max_digits=10, decimal_places=2)

    def get_absolute_url(self):
        return reverse("payment:payment_detail", args=[str(self.id)])
