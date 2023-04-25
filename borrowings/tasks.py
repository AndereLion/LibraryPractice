import asyncio
from datetime import datetime, timedelta


from celery import shared_task


@shared_task
def check_borrowing_overdue():
    from library_bot.bot import bot
    from library_bot.settings import settings
    from borrowings.models import Borrowing

    tomorrow = datetime.today().date() + timedelta(days=1)
    overdue_borrowings = Borrowing.objects.filter(
        expected_return_date__lte=tomorrow, actual_return_date__isnull=True
    )
    if overdue_borrowings:
        message = "The following books are overdue:\n"
        for borrowing in overdue_borrowings:
            message += f"{borrowing.book.title} - {borrowing.user.email}\n"
        asyncio.run(bot.send_message(chat_id=settings.CHAT_ID, text=message))
    else:
        asyncio.run(bot.send_message(chat_id=settings.CHAT_ID, text="No overdue books!"))
