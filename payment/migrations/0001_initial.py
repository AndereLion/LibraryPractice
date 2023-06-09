# Generated by Django 4.2 on 2023-04-25 16:05

from django.db import migrations, models
import payment.models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            (payment.models.PaymentStatus["PENDING"], "Pending"),
                            (payment.models.PaymentStatus["PAID"], "Paid"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            (payment.models.PaymentType["PAYMENT"], "Payment"),
                            (payment.models.PaymentType["FINE"], "Fine"),
                        ],
                        max_length=50,
                    ),
                ),
                ("borrowing_id", models.PositiveIntegerField()),
                ("session_url", models.URLField()),
                ("session_id", models.CharField(max_length=100)),
                ("money_to_pay", models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
