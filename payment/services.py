import os

import stripe

from django.urls import reverse
from django.http import HttpRequest

from payment.models import Payment, PaymentStatus, PaymentType


def calculate_borrowing_total_price(borrowing):
    days = calculate_borrowing_days(borrowing)
    borrowing_total_price = days * borrowing.book.daily_fee
    return round(borrowing_total_price, 2)


def calculate_borrowing_days(borrowing):
    if not borrowing.actual_return_date or (
            borrowing.expected_return_date
            < borrowing.actual_return_date
    ):
        return 0
    days_in_dept = (borrowing.expected_return_date
                    - borrowing.actual_return_date).days + 1
    return days_in_dept


def create_borrowing_stripe_session(borrowing):
    request = HttpRequest()
    success_url = request.build_absolute_uri(reverse("payment:order_success"))
    cancel_url = request.build_absolute_uri(reverse("payment:order_cancel"))
    checkout_session = stripe.checkout.Session.create(

        success_url=success_url + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=cancel_url,
        payment_method_types=["card"],
        mode="subscription",
        api_key=os.environ.get("STRIPE_SECRET_KEY"),
        line_items=[
            {
                "price": borrowing.book.stripe_price_key,
                "quantity": calculate_borrowing_days(borrowing),
            }
        ]
    )
    payment_obj = Payment.objects.create(
        status=PaymentStatus.PENDING,
        type=PaymentType.PAYMENT,
        borrowing_id=borrowing.id,
        session_url=checkout_session["url"],
        session_id=checkout_session["id"],
        money_to_pay=calculate_borrowing_total_price(borrowing),
    )
    return checkout_session, payment_obj
