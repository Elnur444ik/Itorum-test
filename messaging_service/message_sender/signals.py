from datetime import datetime
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Mailing, Client, Message
from .tasks import send_message
from datetime import datetime
import pytz

local = pytz.timezone('Europe/Moscow')


@receiver(post_save, sender=Mailing, dispatch_uid="create_message")
def create_message(sender, instance, created, **kwargs):
    if created:
        mailing = Mailing.objects.filter(id=instance.id).first()
        if mailing.mobile_operator_code or mailing.client_tag:
            clients = Client.objects.filter(
                Q(mobile_operator_code=mailing.mobile_operator_code) | Q(client_tag=mailing.client_tag)
            ).all()
        else:
            clients = Client.objects.all()

        for client in clients:

            if mailing.start_datetime <= datetime.now() <= mailing.end_datetime:
                send_message.apply_async((client.id, mailing.id), expires=mailing.end_datetime)
            else:
                naive = datetime.strptime(str(mailing.start_datetime), "%Y-%m-%d %H:%M:%S")
                local_dt = local.localize(naive, is_dst=None)
                utc_start_time = local_dt.astimezone(pytz.utc)
                send_message.apply_async((client.id, mailing.id), eta=utc_start_time,
                                         expires=mailing.end_datetime)
