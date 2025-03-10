# Generated by Django 4.2.9 on 2024-06-22 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TradeSignals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('script_name', models.CharField(blank=True, max_length=255, null=True)),
                ('price', models.BigIntegerField(blank=True, null=True)),
                ('strike_price', models.BigIntegerField(blank=True, null=True)),
                ('type', models.CharField(blank=True, choices=[('Buy', 'BUY'), ('Sell', 'SELL')], max_length=5, null=True)),
            ],
        ),
    ]
