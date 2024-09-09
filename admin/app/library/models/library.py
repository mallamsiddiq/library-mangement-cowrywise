from datetime import timedelta

from django.db import models, transaction
from django.utils import timezone

from utils.models import AuditableModel
from library.models.enums import PublisherChoices, CategoryChoices


class Book(AuditableModel):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, default= '')
    publisher = models.CharField(
        max_length=50,
        choices=PublisherChoices.choices()
    )
    category = models.CharField(
        max_length=50,
        choices=CategoryChoices.choices()
    )
    total_copies = models.PositiveIntegerField(default=1)
    copies_borrowed = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.title} by {self.author}"

    @property
    def available_copies(self):
        return self.total_copies - self.copies_borrowed
    
    @property
    def expected_return_date(self):
        latest_return_date = self.issuances.filter(returned_at__isnull=True)\
            .aggregate(return_date = models.Max('date_to_return'))['return_date']
        return latest_return_date or None


class Issuance(AuditableModel):
    user = models.ForeignKey('authapp.User', on_delete=models.CASCADE, 
                             related_name='book_issuances')
    book = models.ForeignKey('Book', on_delete=models.CASCADE, 
                             related_name='issuances')
    date_to_return = models.DateTimeField()
    returned_at = models.DateTimeField(null=True, blank=True, db_index=True)

    def __str__(self):
        return f"Issued: {self.book.title} to {self.user.firstname} {self.user.lastname}"

