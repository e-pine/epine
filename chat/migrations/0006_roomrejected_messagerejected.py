# Generated by Django 4.2.4 on 2023-11-28 11:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0005_messagelow'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoomRejected',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='MessageRejected',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages_rejected', to='chat.roomlowquality')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages_rejected', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('date_added',),
            },
        ),
    ]