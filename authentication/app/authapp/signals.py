from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


from authapp.models import User
from events.producers.send_users_updates import send_users_event


@receiver(post_save, sender=User)
def user_updates_handler(sender, instance, created, **kwargs):
    
    if not getattr(instance, 'from_event_boss', False): 
        
        if created:
            # Call task to send event to RabbitMQ
            send_users_event(instance, 'create')
            
        else:
            send_users_event(instance, 'update')


