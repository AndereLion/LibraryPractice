from django.urls import path
from payment import views
from payment.views import order_success, order_cancel

urlpatterns = [
    path("payments/", views.payment_list, name="payment_list"),
    path("payments/<int:pk>/", views.payment_detail, name="payment_detail"),
    path('order/success/', order_success, name="order_success"),
    path('order/cancel/', order_cancel, name="order_cancel"),
    path("config/", views.stripe_config),
    path("create-borrowing-checkout-session/<int:borrowing_id>/", views.create_checkout_session),
    path("webhook", views.stripe_webhook),
]

app_name = "payment"
