# Generated by Django 4.2.9 on 2024-05-23 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_client_client_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='client_password',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
