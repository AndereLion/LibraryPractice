# Generated by Django 4.2 on 2023-04-26 11:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("books", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="stripe_price_key",
            field=models.CharField(default="", max_length=100),
            preserve_default=False,
        ),
    ]
