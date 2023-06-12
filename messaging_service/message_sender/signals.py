from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Mailing, Client, Message
from .tasks import send_message
from datetime import datetime
import pytz
import logging

local = pytz.timezone('Europe/Moscow')


@receiver(post_save, sender=Mailing, dispatch_uid="create_message")
def create_message(sender, instance, created, **kwargs):
    if created:
        clients = Client.objects.filter(
            Q(mobile_operator_code=instance.mobile_operator_code) | Q(client_tag=instance.client_tag)
        ).all() if instance.mobile_operator_code or instance.client_tag else []
        if clients:
            for client in clients:
                if instance.start_datetime <= datetime.now() <= instance.end_datetime:
                    send_message.apply_async((client.id, instance.id), expires=instance.end_datetime)
                else:
                    naive = datetime.strptime(str(instance.start_datetime), "%Y-%m-%d %H:%M:%S")
                    local_dt = local.localize(naive, is_dst=None)
                    utc_start_time = local_dt.astimezone(pytz.utc)
                    send_message.apply_async((client.id, instance.id), eta=utc_start_time,
                                             expires=instance.end_datetime)
        else:
            logging.info(f'Клиенты, подходящие под фильтры отсутствуют, рассылка сообщений отменена')

