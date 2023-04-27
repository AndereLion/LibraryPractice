import asyncio

from django.db.models.signals import post_save
from django.dispatch import receiver
from payment.models import Payment, PaymentStatus


@receiver(post_save, sender=Payment)
def send_notification(sender, instance, created, **kwargs):
    from library_bot.bot import bot
    from library_bot.settings import settings

    if instance.status == PaymentStatus.PAID:
        try:
            message = (
                f"Payment was successfully paid! \n"
                f"PAYMENT ID: {instance.id}\n"
                f"BORROWING ID: {instance.borrowing_id}\n"
                f"Money to pay: ${instance.money_to_pay}"
            )
            asyncio.run(bot.send_message(chat_id=settings.CHAT_ID, text=message))
        except:
            pass
