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

    def test_borrow_method(self):
        # Test that borrowing increases the count of borrowed copies
        self.book.borrow()
        self.assertEqual(self.book.copies_borrowed, 1)

        # Test that it cannot borrow more than available copies
        for _ in range(4):
            self.book.borrow()
        self.assertEqual(self.book.copies_borrowed, 5)

        # Attempting to borrow again should not change the count
        self.book.borrow()
        self.assertEqual(self.book.copies_borrowed, 5)

    def test_return_book_method(self):
        self.book.copies_borrowed += 4
        self.book.save()
        self.book.refresh_from_db()
        
        for idx in range(total:=int(self.book.copies_borrowed)):
            self.book.return_book()
            self.assertEqual(self.book.copies_borrowed, total - idx - 1)
            
        self.assertEqual(self.book.copies_borrowed, 0)

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


class IssuanceModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            firstname='John', lastname='Doe', email='john.doe@example.com', password='password123'
        )
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            publisher='Test Publisher',
            category='Fiction',
            total_copies=5
        )
        self.issuance = Issuance.objects.create(
            user=user,
            book=self.book
        )

    def test_mark_returned_method(self):
        # Ensure that marking as returned updates the return date and book count
        self.issuance.mark_returned()
        self.assertIsNotNone(self.issuance.returned_at)
        self.assertEqual(self.book.copies_borrowed, 0)

    def test_is_returned_property(self):
        # Test the is_returned property
        self.assertFalse(self.issuance.is_returned)
        self.issuance.mark_returned()
        self.assertTrue(self.issuance.is_returned)

    def test_is_overdue_property(self):
        # Test that an overdue issuance is recognized
        self.issuance.returned_at = None
        self.issuance.date_to_return = timezone.now() - timezone.timedelta(days=1)
        self.assertTrue(self.issuance.is_overdue)

        # Test that a non-overdue issuance is recognized
        self.issuance.returned_at = None
        self.issuance.date_to_return = timezone.now() + timezone.timedelta(days=1)
        self.assertFalse(self.issuance.is_overdue)