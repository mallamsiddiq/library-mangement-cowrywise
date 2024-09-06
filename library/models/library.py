from datetime import timedelta

from django.db import models
from django.utils import timezone

from utils.models import AuditableModel
from library.models.enums import PublisherChoices, CategoryChoices


class Book(AuditableModel):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publisher = models.CharField(
        max_length=50,
        choices=PublisherChoices.choices()
    )
    category = models.CharField(
        max_length=50,
        choices=CategoryChoices.choices()
    )
    total_copies = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.title} by {self.author}"

    @property
    def available_copies(self):
        issued_books = self.issuances.filter(returned_at__isnull=True).count()
        return self.total_copies - issued_books

    def is_available(self):
        return self.available_copies > 0


class Issuance(AuditableModel):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, 
                             related_name='book_issuances')
    book = models.ForeignKey('Book', on_delete=models.CASCADE, 
                             related_name='issuances')
    issued_at = models.DateTimeField(auto_now_add=True)
    return_by = models.DateField(default=timezone.now() + timedelta(days=7))
    returned_at = models.DateTimeField(null=True, blank=True, db_index=True)

    def __str__(self):
        return f"Issued: {self.book.title} to {self.user.first_name} {self.user.last_name}"

    def save(self, *args, **kwargs):
        if self._state.adding and not self.book.is_available():
            raise ValueError(f"The book {self.book.title} is not available for borrowing.")
        super().save(*args, **kwargs)

    def mark_returned(self):
        self.returned_at = timezone.now()
        self.save(update_fields=['returned_at'])
