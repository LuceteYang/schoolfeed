# Generated by Django 2.0.13 on 2019-04-24 13:06

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('schools', '0002_auto_20190424_1303'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SchoolMember',
            new_name='Member',
        ),
    ]