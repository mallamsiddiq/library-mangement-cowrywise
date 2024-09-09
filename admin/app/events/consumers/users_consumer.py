
import json, sys, os

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, os.path.join(BASE_DIR, 'app'))

from events.consumers.common import start_event_consumer, event_callback
from authapp.models import User
from events.utils.serializers import UsersSerializer

def callback(ch, method, properties, body):
    
    message = json.loads(body)
    return event_callback(message, User, UsersSerializer)

if __name__ == '__main__':
    start_event_consumer(queue_name='frontend_users_updates', callback=callback)

