from django.test import TestCase
from django.utils import timezone
from library.models import Book, Issuance
from authapp.models import User  # Adjust this import based on your User model location


class BookModelTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            publisher='Test Publisher',
            category='Fiction',
            total_copies=5,
            copies_borrowed=0
        )

    def test_expected_return_date_property(self):
        user = User.objects.create_user(
            firstname='John', lastname='Doe', email='john.doe@example.com', password='password123'
        )
        issuance = Issuance.objects.create(user=user, book=self.book)
        expected_date = issuance.date_to_return
        self.assertEqual(self.book.expected_return_date, expected_date)

        # If there are no active issuances, it should return None
        issuance.returned_at = timezone.now()
        issuance.save()
        self.assertIsNone(self.book.expected_return_date)

