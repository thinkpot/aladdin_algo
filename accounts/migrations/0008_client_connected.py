# Generated by Django 4.2.9 on 2024-05-23 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_client_totp'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='connected',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
