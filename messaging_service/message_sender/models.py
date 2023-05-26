from datetime import datetime
from .validators import phone_regex_validator, code_regex_validator
from django.db import models
from rest_framework.exceptions import ValidationError


class Mailing(models.Model):
    """Сущность рассылка"""

    message_text = models.TextField(verbose_name='Текст сообщения для доставки клиенту')
    mobile_operator_code = models.CharField(max_length=3, validators=[code_regex_validator],
                                            verbose_name="Код мобильного оператора", blank=True, null=True
                                            )
    client_tag = models.CharField(max_length=50, verbose_name="Тэг клиента", blank=True, null=True)
    start_datetime = models.DateTimeField(verbose_name='Дата и время запуска')
    end_datetime = models.DateTimeField(verbose_name='Дата и время окончания')

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    def __str__(self):
        return f'{self.start_datetime} - {self.message_text}'

    def clean(self, *args, **kwargs):
        if self.start_datetime > self.end_datetime:
            raise ValidationError('Дата начала рассылки не может быть меньше даты окончания')
        if self.end_datetime < datetime.now():
            raise ValidationError('Дата окончания рассылки не может быть меньше текущей даты')
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Client(models.Model):
    """Сущность клиент"""

    phone_number = models.CharField(
        verbose_name="Номер телефона клиента", max_length=11,
        validators=[phone_regex_validator], unique=True,
    )
    mobile_operator_code = models.CharField(
        max_length=3, verbose_name="Код мобильного оператора",
        validators=[code_regex_validator],
    )
    client_tag = models.CharField(max_length=50, verbose_name="Тэг клиента", blank=True, null=True)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        if self.client_tag:
            return f'{self.phone_number} - {self.client_tag}'
        return f'{self.phone_number}'


class Message(models.Model):
    """Сущность сообщение"""

    create_datetime = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания (отправки)')
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name="id рассылки")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="id клиента")

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return f'{self.create_datetime} - {self.mailing} - {self.client}'
