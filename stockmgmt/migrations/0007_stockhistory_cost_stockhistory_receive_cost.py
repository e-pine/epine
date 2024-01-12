# Generated by Django 4.2.4 on 2023-09-26 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockmgmt', '0006_stock_receive_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockhistory',
            name='cost',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='stockhistory',
            name='receive_cost',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
