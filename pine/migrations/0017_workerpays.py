# Generated by Django 4.2.4 on 2023-10-11 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pine', '0016_pineprice_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkerPays',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('price_pay', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('date', models.DateField(null=True)),
            ],
        ),
    ]
