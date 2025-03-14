from django.db import models

#predefined user model of django
from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model):
    name=models.CharField(max_length=200)
    def __str__(self):
        return self.name


class Room(models.Model):
    #one topic can have multiple rooms
    topic=models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    host=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants=models.ManyToManyField(User, related_name='participants')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField (auto_now_add=True)
    class Meta:
        ordering = ['-created']  # Show newest rooms first

    def __str__(self):
        return self.name
    

class Message(models.Model):
    #one to many relationship
    #one user can have many messages
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room= models.ForeignKey(Room, on_delete=models.CASCADE)
    body=models.TextField()

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField (auto_now_add=True)
    def __str__(self):
        return self.body