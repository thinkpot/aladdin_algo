from django.contrib import admin
from .models import Broker, Client

# Register your models here.
admin.site.register(Broker)
admin.site.register(Client)