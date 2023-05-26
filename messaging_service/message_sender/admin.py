from django.contrib import admin
from .models import Mailing, Client, Message

admin.site.register(Client)
admin.site.register(Message)
admin.site.register(Mailing)
