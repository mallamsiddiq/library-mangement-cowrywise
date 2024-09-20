import pika
import json
from django.conf import settings

def publish_to_network(message, queue, exchange = None):
    
    
    AMQP_URL = getattr(settings, 'AMQP_URL')
    url_params = pika.URLParameters(AMQP_URL)
 
    connection = pika.BlockingConnection(url_params)
    channel = connection.channel()
    
    exchange = exchange or 'users_events'
    
    # Declare a queue to send the message to
    channel.queue_declare(queue=queue, durable=True)

    message = message

    # Publish the message to the RabbitMQ queue
    channel.basic_publish(exchange=exchange,
                          routing_key=queue,
                          body=json.dumps(message),
                          properties=pika.BasicProperties(
                              delivery_mode=2
                          ))
    
    connection.close()
    