from django.urls import path
from payment import views

urlpatterns = [
    path('payments/', views.PaymentListAPIView.as_view(), name='payment_list'),
    path('payments/<int:pk>/', views.PaymentDetailAPIView.as_view(), name='payment_detail'),

    path('', views.HomePageView.as_view(), name='home'),
    path('config/', views.stripe_config),
    path('create-checkout-session/', views.create_checkout_session),
    path('success/', views.SuccessView.as_view()),
    path('cancelled/', views.CancelledView.as_view()),
    path('webhook/', views.stripe_webhook),
]

app_name = "payment"
