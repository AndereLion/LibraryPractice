from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=100, unique=True)
    author = models.CharField(max_length=100)
    # implement book cover choices with enum

    cover_choice = (
        ("H", "Hard"),
        ("S", "Soft"),
    )
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self) -> str:
        return self.title
