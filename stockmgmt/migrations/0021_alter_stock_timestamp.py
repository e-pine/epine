# Generated by Django 4.2.4 on 2023-10-24 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockmgmt', '0020_alter_stock_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]