from django.db import models
# from accounts.models import User
from django.contrib.auth import get_user_model
# Create your models here.


User = get_user_model()
class Post(models.Model):
    '''
    this is a class to define posts for blog app
    '''
    auther = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="post", null=True, blank=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    status = models.BooleanField()
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField()

    def __str__(self):
        return self.title[:50]
    

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name