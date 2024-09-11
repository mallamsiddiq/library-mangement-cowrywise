import pika, logging, time, os, sys, django
from django.conf import settings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, os.path.join(BASE_DIR, 'app'))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from events.utils.utils import event_bus_context


logger = logging.getLogger(__name__)


def event_callback(message, ModelClass, SerializerClass):
    model_id = message.get('id')
    
    if message['event'] in {'create', 'update'}:
        with event_bus_context(ModelClass):
            partial = message['event'] == 'update'
            serializer = SerializerClass(data=message, partial=partial)
            serializer.is_valid(raise_exception=True)
            
            instance = ModelClass.objects.filter(id=model_id)

            if instance:
                # If the instance exists, update it
                instance.update(**dict(serializer.validated_data))  # Save the updates to the database
                created = False
            else:
                # If the instance does not exist, create a new one
                instance = ModelClass.objects.create(**dict(serializer.validated_data))
                created = True
            
            print(f"{ModelClass.__name__} {model_id} {'created' if created else 'updated'}: {instance}")
    
    elif message['event'] == 'deleted':
        with event_bus_context(ModelClass):
            ModelClass.objects.filter(id=model_id).delete()
            print(f"{ModelClass.__name__} {model_id} deleted")


def start_event_consumer(queue_name, callback, max_retries=10, retry_delay=5):
    """Start the event consumer with retry mechanism on connection failures."""
    
    AMQP_URL = getattr(settings, 'AMQP_URL')
    url_params = pika.URLParameters(AMQP_URL)

    retries = 0
    
    while retries < max_retries:
        try:
            # Establish the connection
            connection = pika.BlockingConnection(url_params)
            channel = connection.channel()

            # Declare the exchange and queue
            channel.exchange_declare(exchange='admin_events', exchange_type='direct')
            channel.queue_declare(queue=queue_name)
            channel.queue_bind(exchange='admin_events', queue=queue_name, routing_key=queue_name)

            # Start consuming messages
            channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
            print(f"Waiting for messages on {queue_name}. To exit press CTRL+C")
            retries = 0
            channel.start_consuming()
            
        except (pika.exceptions.AMQPConnectionError, pika.exceptions.ChannelError) as e:
            retries += 1
            logger.error(f"Connection failed: {e}. Retrying {retries}/{max_retries} in {retry_delay} seconds...")
            
            if retries < max_retries:
                time.sleep(retry_delay)  # Wait before retrying
            else:
                logger.error(f"Max retries reached. Could not establish connection to {AMQP_URL}")
                break
        except KeyboardInterrupt:
            print("Consumer interrupted by user, shutting down.")
            try:
                connection.close()
            except Exception:
                pass
            break
