# Generated by Django 4.2.7 on 2023-12-01 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='broadcastnotification',
            name='sent',
            field=models.BooleanField(default=False),
        ),
    ]