# Generated by Django 4.2.4 on 2023-09-26 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockmgmt', '0005_stock_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='receive_cost',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]