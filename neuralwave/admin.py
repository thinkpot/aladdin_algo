from django.contrib import admin
from .models import *
from accounts.models import CustomUser

admin.site.register(ClientAPIDetails)
admin.site.register(ClientProfitLoss)
admin.site.register(CustomUser)