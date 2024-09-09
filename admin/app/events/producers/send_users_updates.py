from .publisher import publish_to_network
from ..utils.serializers import UsersSerializer


def send_user_event(book_instance, event):
    
    book_data = UsersSerializer(book_instance).data

    # Add event type
    book_data['event'] = event
    
    message = book_data
    
    publish_to_network(message, 'admin_users_updates')
