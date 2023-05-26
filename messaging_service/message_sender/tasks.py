from datetime import datetime

from celery.utils.log import get_task_logger

from messaging_service.celery import app
from .models import Message, Client, Mailing


@app.task
def send_message(message_id, client_id, mailing_id):
    message = Message.objects.get(pk=message_id)
    client = Client.objects.get(pk=client_id)
    mailing = Mailing.objects.get(pk=mailing_id)

    if mailing.start_datetime <= datetime.now() <= mailing.end_datetime:
        # Вводим дополнительную проверку из-за особенности работы eta в celery
        print(f'{datetime.now()}: Сообщение {message.id} отправлено на номер {client.phone_number} по рассылке '
              f'№ {mailing.id}')

