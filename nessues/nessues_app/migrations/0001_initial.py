# Generated by Django 3.1.3 on 2021-04-12 19:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=21)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('description', models.CharField(max_length=32)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('room', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='nessues_app.room')),
                ('text', models.CharField(max_length=120)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('created_by', models.IntegerField()),
                ('group', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
            ],
        ),
    ]
