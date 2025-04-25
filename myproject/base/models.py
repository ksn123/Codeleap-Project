from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=200)
    created_datetime = models.DateTimeField(auto_now_add=True)

class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created_datetime = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=1500)
    
