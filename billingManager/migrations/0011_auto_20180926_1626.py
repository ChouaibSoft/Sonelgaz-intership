# Generated by Django 2.0 on 2018-09-26 16:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('billingManager', '0010_auto_20180926_1023'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='user_first_name',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='user_last_name',
        ),
    ]
