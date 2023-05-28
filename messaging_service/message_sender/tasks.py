from datetime import datetime

from messaging_service.messaging_service.celery import app
from .models import Message, Client, Mailing


@app.task
def send_message(message_id, client_id, mailing_id):
    message = Message.objects.get(pk=message_id)
    client = Client.objects.get(pk=client_id)
    mailing = Mailing.objects.get(pk=mailing_id)

    if datetime.now() <= mailing.end_datetime:
        # Вводим дополнительную проверку из-за особенности работы eta в celery
        print(f'{datetime.now()}: Сообщение {message.id} отправлено на номер {client.phone_number} по рассылке '
              f'№ {mailing.id}')
    else:
        print(f'{datetime.now()}: Сообщение {message.id} не было отправлено на номер {client.phone_number}, '
              f'так как закончилось время рассылки № {mailing.id}')

