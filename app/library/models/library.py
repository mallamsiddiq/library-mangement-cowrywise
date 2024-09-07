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

    def is_available(self):
        return self.available_copies > 0
    
    def borrow(self):
        """
        Increases the borrowed copies by 1
        """
        if self.is_available():
            self.copies_borrowed += 1
            self.save(update_fields=['copies_borrowed'])

    def return_book(self):
        """
        Reduces the borrowed copies by 1
        """
        self.copies_borrowed -= 1
        self.save(update_fields=['copies_borrowed'])


class Issuance(AuditableModel):
    user = models.ForeignKey('authapp.User', on_delete=models.CASCADE, 
                             related_name='book_issuances')
    book = models.ForeignKey('Book', on_delete=models.CASCADE, 
                             related_name='issuances')
    date_to_return = models.DateTimeField(default=timezone.now() + timedelta(days=7))
    returned_at = models.DateTimeField(null=True, blank=True, db_index=True)

    def __str__(self):
        return f"Issued: {self.book.title} to {self.user.firstname} {self.user.lastname}"

    @transaction.atomic
    def save(self, *args, **kwargs):
        if self._state.adding:
            if not self.book.is_available():
                raise ValueError(f"The book {self.book.title} is not available for borrowing.")
            if Issuance.objects.filter(user=self.user, book=self.book, returned_at__isnull=True).exists():
                raise ValueError(f"The user already has an active issuance for this book.")
            
            self.book.borrow()
    
        super().save(*args, **kwargs)

    @transaction.atomic
    def mark_returned(self):
        self.returned_at = timezone.now()
        self.book.return_book()
        self.save(update_fields=['returned_at'])
        
    @property
    def is_returned(self):
        return bool(self.returned_at is None)
        
    @property
    def is_overdue(self):
        return (not self.is_returned) and timezone.now().date() > self.date_to_return.date()