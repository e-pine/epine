# Generated by Django 4.2.4 on 2023-10-20 10:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pine', '0024_pestonfarm'),
    ]

    operations = [
        migrations.CreateModel(
            name='HarvestedGood',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_buy_pine', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='BiddingProcess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid_price', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('total_buy_pine', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('date', models.DateField(auto_now_add=True, null=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='pine.category')),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]