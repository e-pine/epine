# Generated by Django 4.2.4 on 2023-10-09 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockmgmt', '0014_itemhistory_action'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemhistory',
            name='action',
            field=models.CharField(max_length=50),
        ),
    ]
