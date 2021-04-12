from django.db import models
from django.contrib.auth.models import User, Group


class Room(models.Model):
    name = models.CharField(max_length=21)
    date_created = models.DateField(auto_now_add=True)
    description = models.CharField(max_length=32)
    owner = models.ForeignKey(
        User, 
        null=True, 
        on_delete=models.CASCADE
    )   

class Task(models.Model):
    room = models.OneToOneField(
        Room,
        on_delete=models.CASCADE,
        primary_key=True
    )
    group = models.ForeignKey(
        Group,
        blank=True,      
        on_delete=models.CASCADE
    )
    text = models.CharField(max_length=120)
    date_created = models.DateField(auto_now_add=True)
