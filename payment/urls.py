from django.urls import path
from payment import views

urlpatterns = [
    path("payments/", views.payment_list, name="payment_list"),
    path("payments/<int:pk>/", views.payment_detail, name="payment_detail"),
    path("config/", views.stripe_config),
    path("create-borrowing-checkout-session/<int:borrowing_id>/", views.create_checkout_session),
    path("webhook", views.stripe_webhook),
]

app_name = "payment"
