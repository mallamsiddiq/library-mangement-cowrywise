from events.producers.publisher import publish_to_network
from events.utils.serializers import IssuanceSerializer


def send_borrow_event(borrow_instance, event):
    
    book_data = IssuanceSerializer(borrow_instance).data

    # Add event type
    book_data['event'] = event
    
    message = book_data
    
    publish_to_network(message, 'frontend_borrowing_updates')

