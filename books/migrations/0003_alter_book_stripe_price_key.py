# Generated by Django 4.2 on 2023-04-26 17:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("books", "0002_book_stripe_price_key"),
    ]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="stripe_price_key",
            field=models.CharField(max_length=100, null=True),
        ),
    ]
