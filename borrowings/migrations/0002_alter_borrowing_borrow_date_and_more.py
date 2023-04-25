# Generated by Django 4.2 on 2023-04-25 13:57

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("borrowings", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="borrowing",
            name="borrow_date",
            field=models.DateField(
                validators=[
                    django.core.validators.MinValueValidator(datetime.date(2023, 4, 25))
                ]
            ),
        ),
        migrations.AlterField(
            model_name="borrowing",
            name="expected_return_date",
            field=models.DateField(
                validators=[
                    django.core.validators.MinValueValidator(datetime.date(2023, 4, 25))
                ]
            ),
        ),
    ]
