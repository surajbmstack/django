from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Topic(models.Model):
    name=models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
  

class Room(models.Model):
    host=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    topic=models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True)
    name=models.CharField(max_length=50)
    description=models.TextField(null=True,blank=True)
    # participants=models.IntegerField(default=0)
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)
    participants=models.ManyToManyField(User,related_name='participants')
    class Meta:
        ordering=['-created','-updated']
    
    def __str__(self):
        return self.name

   


class Message(models.Model):
   user=models.ForeignKey(User,on_delete=models.CASCADE)
   room=models.ForeignKey(Room,on_delete=models.CASCADE)
   body=models.TextField()
   updated=models.DateTimeField(auto_now=True)
   created=models.DateTimeField(auto_now_add=True)
   class Meta:
        ordering=['-created','-updated']
   def __str__(self):
       return self.body[:50]
  
