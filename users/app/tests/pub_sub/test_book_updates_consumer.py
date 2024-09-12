import json
import uuid
from events.consumers.book_consumer import callback
from django.test import TestCase
from library.models import Book

class TestBookEventConsumer(TestCase):
    
    def test_book_update_event(self):
        # Create a message representing a "create" event
        message = {
            'id': str(uuid.uuid4()),
            'title': 'Test Book', 
            'author': 'Test Author', 
            'publisher': 'Wiley', 
            'category': 'Fiction',
            'total_copies': 10, 
            'copies_borrowed': 0,
            'created_at': '2024-09-11T00:00:00Z',
            'updated_at': '2024-09-11T00:00:00Z',
            'event': 'create'
        }
        
        # Ensure no books exist before the callback is executed
        self.assertEqual(Book.objects.count(), 0)
        
        # Call the callback function with the mock message
        callback(None, None, None, json.dumps(message))
        
        # Retrieve the created book instance
        created_book = Book.objects.filter(id=message['id']).first()
        
        # Assert the book instance was created
        self.assertIsNotNone(created_book, "Book instance was not created.")
        
        # Assert each field is set correctly
        self.assertEqual(created_book.title, message['title'])
        self.assertEqual(created_book.author, message['author'])
        self.assertEqual(created_book.publisher, message['publisher'])
        self.assertEqual(created_book.category, message['category'])
        self.assertEqual(created_book.total_copies, message['total_copies'])
        self.assertEqual(created_book.copies_borrowed, message['copies_borrowed'])