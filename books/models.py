from django.db import models


class Book(models.Model):
    class CoverChoices(models.TextChoices):
        SOFT = "SOFT"
        HARD = "HARD"
    title = models.CharField(max_length=100, unique=True)
    author = models.CharField(max_length=100)
    cover = models.CharField(max_length=4, choices=CoverChoices.choices)
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(max_digits=5, decimal_places=2)
    stripe_price_key = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.title
