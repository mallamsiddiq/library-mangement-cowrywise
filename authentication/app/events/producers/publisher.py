import pika
import json
from django.conf import settings

def publish_to_network(message, routing_key = '', exchange='authapp_events', exchange_type='fanout',):
    """Publish a message to a RabbitMQ exchange with Fanout type."""
    
    AMQP_URL = getattr(settings, 'AMQP_URL')
    url_params = pika.URLParameters(AMQP_URL)
    
    try:
        connection = pika.BlockingConnection(url_params)
        channel = connection.channel()
        
        # Declare the exchange
        channel.exchange_declare(exchange=exchange, exchange_type=exchange_type)
        
        # Publish the message
        channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,  # Fanout exchange ignores routing keys
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2  # Make message persistent
            )
        )
        print(f"Message published to exchange {exchange}.")
    
    except Exception as e:
        print(f"Failed to publish message: {e}")
    
    finally:
        if 'connection' in locals():
            connection.close()
