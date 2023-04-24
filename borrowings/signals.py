from django.db.models.signals import post_save
from django.dispatch import receiver
from borrowings.models import Borrowing

from library_bot.bot import bot, settings


@receiver(post_save, sender=Borrowing)
def send_notification(sender, instance, created, **kwargs):
    if created:
        message = f'A new instance of MyModel was created: {instance}'
        bot.send_message(chat_id=settings.CHAT_ID, text=message)
