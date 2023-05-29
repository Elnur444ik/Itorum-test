# Generated by Django 4.2.1 on 2023-05-28 12:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message_sender', '0004_alter_client_mobile_operator_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailing',
            name='mobile_operator_code',
            field=models.CharField(blank=True, max_length=3, null=True, validators=[django.core.validators.RegexValidator(message='Введен некорректный код оператора', regex='^.{3}$')], verbose_name='Код мобильного оператора'),
        ),
    ]
