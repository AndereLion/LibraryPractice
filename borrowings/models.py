from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from books.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateField(validators=[MinValueValidator(timezone.now().date())])
    expected_return_date = models.DateField(validators=[MinValueValidator(timezone.now().date())])
    actual_return_date = models.DateField(
        validators=[MinValueValidator(timezone.now().date())],
        null=True,
        blank=True,
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def clean(self):
        if self.actual_return_date and self.actual_return_date < timezone.now().date():
            raise ValidationError("Actual return date cannot be earlier than today.")
        if self.expected_return_date < timezone.now().date():
            raise ValidationError("Expected return date cannot be earlier than today.")
        if self.expected_return_date < self.borrow_date:
            raise ValidationError("Expected return date cannot be earlier than borrow date.")

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        if self.actual_return_date:
            return f"Book {self.book} returned at {self.actual_return_date}"
        if self.expected_return_date <= timezone.now().date():
            return f"{self.book} should be returned at {self.expected_return_date}"
        return f"{self.book} overdue for {self.expected_return_date - timezone.now().date()}"
