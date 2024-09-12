from .publisher import publish_to_network
from events.utils.serializers import BookSerializer


def send_book_event(book_instance, event):
    
    book_data = BookSerializer(book_instance).data

    # Add event type
    book_data['event'] = event
    
    message = book_data
    
    publish_to_network(message, 'admin_book_updates')
