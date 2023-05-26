from datetime import datetime
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Mailing, Client, Message
from .tasks import send_message


@receiver(post_save, sender=Mailing)
def create_message(sender, instance, created, *args, **kwargs):
    mailing = Mailing.objects.filter(id=instance.id).first()
    clients = Client.objects.filter(
        Q(mobile_operator_code=mailing.mobile_operator_code) | Q(client_tag=mailing.client_tag)
    ).all()
    for client in clients:
        message = Message.objects.create(mailing=mailing.id, client=client.id)
        if mailing.start_datetime <= datetime.now() <= mailing.end_datetime:
            send_message.apply_async((message.id, client.id, mailing.id), expires=mailing.end_datetime)
        else:
            send_message.apply_async((message.id, client.id, mailing.id), eta=mailing.start_datetime,
                                     expires=mailing.end_datetime)
    else:
        print(f'Рассылка № {mailing.id} завершена')
