import json
from events.consumers.book_consumer import callback
from django.test import TestCase
from library.models import Book


class TestBookEventConsumer(TestCase):
    
    def setUp(self):
    
        self.book = Book.objects.create(
            title=f'Test Book ', 
            author=f'AGBA Author ', 
            publisher='Wiley', 
            category='Fiction',
            total_copies = 1, 
            copies_borrowed=0
        )
    
    def test_book_update_event(self):
        
        message = {
            'id': str(self.book.id),
            'copies_borrowed': 1,
            'event': 'update',
        }
        
        self.assertNotEqual(self.book.copies_borrowed, message['copies_borrowed'])
        callback(None, None, None, json.dumps(message))
        self.book.refresh_from_db()
        self.assertEqual(self.book.copies_borrowed, message['copies_borrowed'])
        
         
        