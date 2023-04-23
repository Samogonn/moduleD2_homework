from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from .models import PostCategory

from .tasks.basic import send_subscription_letter


@receiver(m2m_changed, sender=PostCategory)
def notify_subscribers(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        send_subscription_letter(instance)
