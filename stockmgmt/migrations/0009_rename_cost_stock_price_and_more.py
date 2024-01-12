# Generated by Django 4.2.4 on 2023-10-03 14:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stockmgmt', '0008_alter_stock_cost_alter_stock_receive_cost_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stock',
            old_name='cost',
            new_name='price',
        ),
        migrations.RenameField(
            model_name='stockhistory',
            old_name='cost',
            new_name='price',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='receive_cost',
        ),
        migrations.RemoveField(
            model_name='stockhistory',
            name='receive_cost',
        ),
    ]