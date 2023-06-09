from datetime import datetime

from celery import Celery
from celery.utils.log import get_task_logger
from messaging_service.celery import app
from .models import Message, Client, Mailing

celery = Celery(__name__)
celery.config_from_object(__name__)

logger = get_task_logger(__name__)


@app.task
def send_message(client_id, mailing_id):
    client = Client.objects.get(pk=client_id)
    mailing = Mailing.objects.get(pk=mailing_id)

    message = Message.objects.create(mailing=mailing, client=client)

    if datetime.now() <= mailing.end_datetime:
        # Вводим дополнительную проверку из-за особенности работы eta в celery
        logger.info(f'{datetime.now()}: Сообщение {message.id} отправлено на номер {client.phone_number} по рассылке '
                    f'№ {mailing.id}')
    else:
        logger.info(f'{datetime.now()}: Сообщение {message.id} не было отправлено на номер {client.phone_number}, '
                    f'так как закончилось время рассылки № {mailing.id}')
