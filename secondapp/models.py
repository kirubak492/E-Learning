from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class Topic(models.Model):
    topic=models.CharField(max_length=201)

    def __str__(self):
        return self.topic

class Room(models.Model):

    host=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    topic=models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True)
    name=models.CharField(max_length=200)
    description=models.TextField(null=True, blank=True)
    updated=models.DateTimeField(auto_now=True)#actively updated when submit
    created=models.DateTimeField(auto_now_add=True) #added once created
    
    class Meta:
        ordering=['-updated','-created']
        
    def __str__(self):
        return str(self.name)



class Messages(models.Model):

    user=models.ForeignKey(User,on_delete=models.CASCADE)
    room=models.ForeignKey(Room,on_delete=models.CASCADE)#on_Delete says that if the ROom delete then all the child also deleted
    #foreign key only connect the Room with child(message)
    body=models.TextField()
    updated=models.DateTimeField(auto_now=True)#actively updated when submit
    created=models.DateTimeField(auto_now_add=True) #added once created

    def __str__(self):
        return self.body[0:50]

