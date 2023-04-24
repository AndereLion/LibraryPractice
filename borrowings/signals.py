import asyncio

from django.db.models.signals import post_save
from django.dispatch import receiver
from borrowings.models import Borrowing


from library_bot.bot import bot, settings


@receiver(post_save, sender=Borrowing)
def send_notification(sender, instance, created, **kwargs):
    if created:
        try:
            message = (
                f"New borrowing was successfully created!\n"
                f"Book: {instance.book.title}\n"
                f"User: {instance.user.email}\n"
                f"Expected return date: {instance.expected_return_date}\n"

            )
            asyncio.run(bot.send_message(chat_id=settings.CHAT_ID, text=message))
        except:
            pass
