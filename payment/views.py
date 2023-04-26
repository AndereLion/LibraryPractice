import os

import stripe
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Payment
from .serializers import PaymentListSerializer, PaymentDetailSerializer

from dotenv import load_dotenv
load_dotenv(".env")

#
# class PaymentListAPIView(generics.ListAPIView):
#     serializer_class = PaymentListSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_queryset(self):
#         if self.request.user.is_staff:
#             return Payment.objects.all()
#         else:
#             return Payment.objects.filter(user=self.request.user)
#
#
# class PaymentDetailAPIView(generics.RetrieveAPIView):
#     serializer_class = PaymentDetailSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_queryset(self):
#         if self.request.user.is_staff:
#             return Payment.objects.all()
#         else:
#             return Payment.objects.filter(user=self.request.user)


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
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_checkout_session(request):
    domain_url = "http://localhost:8000/"
    stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
    try:
        checkout_session = stripe.checkout.Session.create(
            client_reference_id=request.user.id if request.user.is_authenticated else None,
            success_url=domain_url + "success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=domain_url + "cancelled/",
            payment_method_types=["card"],
            mode="payment",
            line_items=[
                {
                    "price": os.environ.get("PRICE_KEY"),
                    "quantity": 1,
                }
            ]
        )
        return JsonResponse({"sessionId": checkout_session["id"]})
    except Exception as e:
        return JsonResponse({"error": str(e)})


@api_view(["POST"])
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
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        client_reference_id = session.get("client_reference_id")
        if client_reference_id:
            try:
                payment = Payment.objects.get(pk=client_reference_id)
                payment.status = "paid"
                payment.save()
            except Payment.DoesNotExist:
                pass

    return HttpResponse(status=200)
