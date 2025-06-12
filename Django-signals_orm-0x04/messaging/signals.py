from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.timezone import now
from .models import Message, Notification, MessageHistory

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance,
            is_read=False
        )

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:
        try:
            original = Message.objects.get(pk=instance.pk)
            if original.content != instance.content:
                MessageHistory.objects.create(
                    message=original,
                    old_content=original.content,
                    edited_at=now(),
                    edited_by=instance.sender
                )
                instance.edited = True
        except Message.DoesNotExist:
            pass
