from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email= models.EmailField(null=True, unique=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default="spongebob.jpg")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    pass
    
class Topic(models.Model):
    name = models.CharField(max_length=250)
    def __str__(self):
        return self.name
    
    
class Room(models.Model):
    host = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    topic = models.ForeignKey(Topic,on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=120)
    description = models.TextField(null=True,blank=True)
    participants = models.ManyToManyField(User,related_name='participants', blank=True)
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-update', 'created']
    
    def __str__(self):
        return self.name
    
class Message(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    body = models.TextField()
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]