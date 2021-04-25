# Generated by Django 3.2 on 2021-04-25 10:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('nessues_app', '0004_auto_20210419_1035'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='completed_by',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='table',
            name='date_created',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='task',
            name='date_created',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
