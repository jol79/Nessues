from django.db import models
from django.contrib.auth.models import User, Group


class Room(models.Model):
    name = models.CharField(max_length=21)
    date_created = models.DateField(auto_now_add=True)
    description = models.CharField(max_length=32)
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
    )   

    def __str__(self):
        return self.name
    

class Table(models.Model):
    room = models.ForeignKey(
        Room,
        blank=True,   
        null=True, 
        default=None,  
        on_delete=models.CASCADE
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,  
        default=None,    
        on_delete=models.CASCADE
    )
    date_created = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=21)
    description = models.CharField(max_length=60)

    def __str__(self):
        return self.name


class Task(models.Model):
    table = models.ForeignKey(
        Table,      
        on_delete=models.CASCADE
    )
    text = models.CharField(max_length=120)
    date_created = models.DateField(auto_now_add=True)
    created_by = models.IntegerField(blank=False)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.text
    
