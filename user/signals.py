import asyncio

from django.db.models.signals import post_save
from django.dispatch import receiver
from user.models import User


@receiver(post_save, sender=User)
def send_notification(sender, instance, created, **kwargs):
    from library_bot import bot, settings

    if created:
        try:
            message = (
                f"New user was successfully created!\n"
                f"User email: {instance.email}\n"
                f"First name: {instance.first_name}\n"
            )
            asyncio.run(bot.bot.send_message(chat_id=settings.settings.CHAT_ID, text=message))
        except:
            pass
