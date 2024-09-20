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
            data = dict(serializer.validated_data)
            
            update_kwargs = {'id':data.pop('id')}
            
            if email:=data.pop('email', None):
                update_kwargs.update({'email':email})
            
            instance, created = ModelClass.objects.update_or_create(
                **update_kwargs,
                defaults = data
            )
            
            print(f"{ModelClass.__name__} {model_id} {'created' if created else 'updated'}: {instance}")
    
    elif message['event'] == 'deleted':
        with event_bus_context(ModelClass):
            ModelClass.objects.filter(id=model_id).delete()
            print(f"{ModelClass.__name__} {model_id} deleted")


def start_event_consumer(exchange, queue_name, callback, exchange_type='fanout', max_retries=10, retry_delay=5):
    """Start the event consumer with retry mechanism on connection failures."""
    
    AMQP_URL = getattr(settings, 'AMQP_URL')
    url_params = pika.URLParameters(AMQP_URL)

    retries = 0

    while retries < max_retries:
        try:
            # Establish the connection
            connection = pika.BlockingConnection(url_params)
            channel = connection.channel()

            # Declare the exchange
            channel.exchange_declare(exchange=exchange, exchange_type = exchange_type)

            # Declare and bind the queue
            channel.queue_declare(queue=queue_name, durable=True)
            channel.queue_bind(exchange=exchange, queue=queue_name)

            # Start consuming messages
            channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
            print(f"Waiting for messages on {queue_name}. To exit press CTRL+C")
            retries = 0
            channel.start_consuming()
            
        except (pika.exceptions.AMQPConnectionError, pika.exceptions.ChannelError) as e:
            retries += 1
            print(f"Connection failed: {e}. Retrying {retries}/{max_retries} in {retry_delay} seconds...")
            
            if retries < max_retries:
                time.sleep(retry_delay)  # Wait before retrying
            else:
                print(f"Max retries reached. Could not establish connection to {AMQP_URL[:4]}")
                break
        except KeyboardInterrupt:
            print("Consumer interrupted by user, shutting down.")
            break
        finally:
            if 'connection' in locals():
                connection.close()