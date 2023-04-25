from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import models

from books.models import Book


class Borrowing(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="borrowings"
    )
    user = models.ForeignKey(
        settings.get_user_model(),
        on_delete=models.CASCADE,
        related_name="borrowings"
    )
    borrowed_date = models.DateTimeField(auto_now_add=True)
    expected_return_date = models.DateTimeField()
    actual_return_date = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.user} borrowed {self.book}"

    @property
    def is_active(self) -> bool:
        return self.actual_return_date is None

