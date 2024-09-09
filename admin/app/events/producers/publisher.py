import pika
import json


AMQP_URL = 'amqp://user:password@rabbitmq:/%2F'

url_params = pika.URLParameters(AMQP_URL)

def publish_to_network(message, queue, exchange = None):
    
    exchange = exchange or 'admin_events'
    
    
    connection = pika.BlockingConnection(url_params)
    channel = connection.channel()
    
    # Declare a queue to send the message to
    channel.queue_declare(queue=queue)

    # Prepare the message content (you can send more details about the book)
    message = message

    # Publish the message to the RabbitMQ queue
    channel.basic_publish(exchange=exchange,
                          routing_key=queue,
                          body=json.dumps(message),
                          properties=pika.BasicProperties(
                              delivery_mode=2  # Make message persistent
                          ))
    
    connection.close()