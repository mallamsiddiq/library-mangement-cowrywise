import pika, json, os, sys, django

from django.conf import settings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, os.path.join(BASE_DIR, 'app'))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from events.utils.utils import event_bus_context


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


def start_event_consumer(queue_name, callback):
    AMQP_URL = getattr(settings, 'AMQP_URL')
    url_params = pika.URLParameters(AMQP_URL)

    connection = pika.BlockingConnection(url_params)
    channel = connection.channel()

    # Declare the exchange
    channel.exchange_declare(exchange='users_events', exchange_type='direct')

    # Declare the queue
    channel.queue_declare(queue=queue_name)

    # Bind the queue to the exchange
    channel.queue_bind(exchange='users_events', queue=queue_name, routing_key=queue_name)

    
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    print(f"Waiting for messages on {queue_name}. To exit press CTRL+C")
    channel.start_consuming()
