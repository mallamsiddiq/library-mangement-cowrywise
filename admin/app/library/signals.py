from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from library.models import Book
from authapp.models import User
from events.producers.send_book_updates import send_book_event
from events.producers.send_users_updates import send_user_event


@receiver(post_save, sender=Book)
def book_created_handler(sender, instance, created, **kwargs):
    
    if not getattr(instance, 'from_event_boss', False):
        if created:
            # Call task to send event to RabbitMQ
            send_book_event(instance, 'create')
            
        else:
            send_book_event(instance, 'update')


@receiver(post_delete, sender=Book)
def book_deleted_handler(sender, instance, **kwargs):
    send_book_event(instance, 'deleted')


@receiver(post_save, sender=User)
def user_created_handler(sender, instance, created, **kwargs):
    
    if not getattr(instance, 'from_event_boss', False): 
        
        if created:
            # Call task to send event to RabbitMQ
            send_user_event(instance, 'create')
            
        else:
            send_user_event(instance, 'update')


