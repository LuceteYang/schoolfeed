# Generated by Django 2.0.13 on 2019-05-16 02:57

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('schools', '0005_auto_20190429_1527'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='member_user_set',
            field=models.ManyToManyField(blank=True, related_name='member_user_set', through='schools.Member', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='school',
            name='subscribe_user_set',
            field=models.ManyToManyField(blank=True, related_name='subscribe_user_set', through='schools.Subscribe', to=settings.AUTH_USER_MODEL),
        ),
    ]
