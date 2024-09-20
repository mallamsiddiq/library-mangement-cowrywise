from django.db.models.signals import post_save
from django.dispatch import receiver
from library.models import Book, Issuance
from library.models import User
from events.producers.send_book_updates import send_book_event
from events.producers.send_borrow_updates import send_borrow_event
from events.producers.send_users_updates import send_users_event

@receiver(post_save, sender=Book)
def book_created_handler(sender, instance, created, **kwargs):
    
    if not getattr(instance, 'from_event_boss', False):
        if created:
            send_book_event(instance, 'create')
            
        else:
            send_book_event(instance, 'update')


@receiver(post_save, sender=Issuance)
def issuance_created_handler(sender, instance, created, **kwargs):
    
    
    if not getattr(instance, 'from_event_boss', False):
        
        if created:
            send_borrow_event(instance, 'create')
            
        else:
            send_borrow_event(instance, 'update')


@receiver(post_save, sender=User)
def user_created_handler(sender, instance, created, **kwargs):
    
    if not getattr(instance, 'from_event_boss', False): 
        
        if created:
            
              
            send_users_event(instance, 'create')
            
        else:
            send_users_event(instance, 'update')
