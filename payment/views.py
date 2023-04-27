import os

import stripe
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from . import services

from borrowings.models import Borrowing
from .models import Payment, PaymentStatus
from .serializers import PaymentListSerializer, PaymentDetailSerializer

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def payment_list(request):
    if request.user.is_staff:
        payments = Payment.objects.all()
    else:
        payments = Payment.objects.filter(user=request.user)
    serializer = PaymentListSerializer(payments, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def payment_detail(request, pk):
    if request.user.is_staff:
        payment = Payment.objects.get(pk=pk)
    else:
        payment = Payment.objects.get(pk=pk, user=request.user)
    serializer = PaymentDetailSerializer(payment)
    return Response(serializer.data)


@api_view(["GET"])
def stripe_config(request):
    stripe_config = {"publicKey": os.environ.get("STRIPE_PUBLISHABLE_KEY")}
    return Response(stripe_config)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def order_success(request):
    session_id = request.query_params.get("session_id")
    session = stripe.checkout.Session.retrieve(session_id)
    customer = stripe.Customer.retrieve(session.customer)

    if session.payment_status == "paid":
        payment = Payment.objects.get(session_id=session_id)
        payment.status = PaymentStatus.PAID
        payment.save()

    html = f"<html><body><h1>Thanks for your order, {customer.name}!</h1></body></html>"
    return HttpResponse(html)


@api_view(["GET"])
def order_cancel(request):
    html = ("<html><body><h1>Payment cancelled</h1><p>You can pay later, "
            "but the session is available for only 24 hours.</p></body></html>")
    return HttpResponse(html)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def create_checkout_session(request, borrowing_id: int):
    borrowing = get_object_or_404(Borrowing, pk=borrowing_id)
    if request.method == "GET":
        try:
            checkout_session, _ = services.create_borrowing_stripe_session(borrowing)
            return JsonResponse(checkout_session)
        except Exception as e:
            return JsonResponse({"error": str(e)})


@api_view(["POST"])
@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
    endpoint_secret = os.environ.get("STRIPE_ENDPOINT_SECRET")
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        print("Invalid payload")
        return HttpResponse(status=400)

    except stripe.error.SignatureVerificationError as e:
        print("Invalid signature")
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        print(session)
        session_id = session.get("id")
        print(session_id)
        if session_id:
            try:
                payment = Payment.objects.get(session_id=session_id)
                payment.status = PaymentStatus.PAID
                payment.save()
            except Payment.DoesNotExist:
                print("Payment does not exist")
        else:
            print("Session id does not exist")

    return HttpResponse(status=200)
