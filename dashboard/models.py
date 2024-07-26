from django.db import models


class TradeSignals(models.Model):
    script_name = models.CharField(max_length=255, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    strike_price = models.BigIntegerField(null=True, blank=True)
    type = models.CharField(max_length=5, null=True, blank=True, choices=(('Buy', 'BUY'),
                                                                          ('Sell', 'SELL')))