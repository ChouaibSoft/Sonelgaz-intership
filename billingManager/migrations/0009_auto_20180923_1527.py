# Generated by Django 2.0 on 2018-09-23 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billingManager', '0008_auto_20180923_1451'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bill',
            name='rejection_reasonBO',
        ),
        migrations.AddField(
            model_name='bill',
            name='rejection_reasonBO',
            field=models.ManyToManyField(related_name='motif1', to='billingManager.RejectionReason'),
        ),
        migrations.RemoveField(
            model_name='bill',
            name='rejection_reasonFC',
        ),
        migrations.AddField(
            model_name='bill',
            name='rejection_reasonFC',
            field=models.ManyToManyField(related_name='motif3', to='billingManager.RejectionReason'),
        ),
        migrations.RemoveField(
            model_name='bill',
            name='rejection_reasonST',
        ),
        migrations.AddField(
            model_name='bill',
            name='rejection_reasonST',
            field=models.ManyToManyField(related_name='motif2', to='billingManager.RejectionReason'),
        ),
    ]
