from rest_framework import serializers

from payment.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class PaymentListSerializer(PaymentSerializer):
    class Meta:
        model = Payment
        fields = (
            "id",
            "status",
            "type",
            "borrowing_id",
            "money_to_pay"
        )


class PaymentDetailSerializer(PaymentSerializer):

    class Meta:
        model = Payment
        fields = "__all__"
