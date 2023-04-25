from django.urls import path
<<<<<<< HEAD
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
=======
from .views import PaymentListAPIView, PaymentDetailAPIView

urlpatterns = [
    path('payments/', PaymentListAPIView.as_view(), name='payment_list'),
    path('payments/<int:pk>/', PaymentDetailAPIView.as_view(), name='payment_detail'),
>>>>>>> 2ff7d1d420c81fa51c21540c2a163ae98a44021e
]

app_name = "payment"
