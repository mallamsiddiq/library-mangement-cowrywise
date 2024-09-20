import uuid, pika
from unittest import mock, TestCase
from library.models import Book
from django.conf import settings

from django.test import TestCase


AMQP_URL = getattr(settings, 'AMQP_URL')
url_params = pika.URLParameters(AMQP_URL)
      
        
class TestBookEventProducer(TestCase):
    
    @mock.patch('events.producers.publisher.pika.BlockingConnection')
    def test_send_book_event_update(self, mock_publish_to_network):
        # Mock a book instance
        book = Book(
            id = str(uuid.uuid4()),
            title=f'Test Book', author='Test Author', 
            publisher='Wiley', 
            category='Fiction',
            total_copies=10, copies_borrowed=0
        )
        
        # Call the event producer
        # send_book_event(book, 'update')
        book.save()
        
        # Verify that publish_to_network was called with the correct arguments
        mock_publish_to_network.assert_called_once_with(
            url_params
        )

