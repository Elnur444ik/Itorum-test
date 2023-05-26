from django.shortcuts import render
from rest_framework import viewsets
from .serializers import MailingSerializer, ClientSerializer, MessageSerializer
from .models import Mailing, Message, Client


class MailingViewSet(viewsets.ModelViewSet):
    """Представление сущности рассылка"""

    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer


class ClientViewSet(viewsets.ModelViewSet):
    """Представление сущности клиент"""

    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class MessageViewSet(viewsets.ModelViewSet):
    """Представление сущности сообщение"""

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
