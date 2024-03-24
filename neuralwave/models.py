from django.db import models
from .validators import validate_phone_number


class ClientAPIDetails(models.Model):
    name = models.CharField(max_length=254, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=12, validators=[validate_phone_number], null=True, blank=True)
    api_key = models.TextField(null=True, blank=True)
    api_secret = models.TextField(null=True, blank=True)
    totp_key = models.TextField(null=True, blank=True)
    purchase_date = models.DateTimeField(null=True, blank=True)
    broker = models.CharField(max_length=255, choices=(
        ('ALICEBLUE', 'ALICEBLUE'),
        ('UPSTOCK', 'UPSTOCK'),
        ('ANGELONE', 'ANGELONE'),
        ('ZERODHA', 'ZERODHA')
    ), null=True, blank=True)
    broker_id = models.CharField(max_length=255, null=True, blank=True)
    broker_password = models.CharField(max_length=255, null=True, blank=True)
    broker_pin = models.IntegerField(null=True, blank=True)


    def __str__(self):
        return f"{self.phone} {self.email}"


class ClientProfitLoss(models.Model):
    client = models.ForeignKey('ClientAPIDetails', on_delete=models.DO_NOTHING, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profit = models.BigIntegerField(null=True, blank=True, default=0)
    loss = models.BigIntegerField(null=True, blank=True, default=0)
    symbol = models.CharField(max_length=255, choices=(
        ('NIFTY', 'NIFTY'),
        ('BANKNIFTY', 'BANKNIFTY'),
        ('OTHERS', 'OTHERS')
    ))