# Generated by Django 4.2.4 on 2023-10-07 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pine', '0008_remove_pinevalue_name_pinevalue_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='yield',
            name='pr',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
