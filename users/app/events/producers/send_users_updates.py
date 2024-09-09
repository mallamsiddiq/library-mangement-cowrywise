from events.producers.publisher import publish_to_network
from events.utils.serializers import UsersSerializer


def send_users_event(user_instance, event):
    
    book_data = UsersSerializer(user_instance).data

    # Add event type
    book_data['event'] = event
    
    message = book_data
    
    publish_to_network(message, 'frontend_users_updates')
