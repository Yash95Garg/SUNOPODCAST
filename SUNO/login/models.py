from django.db import models
from django.contrib.auth.models import User

User._meta.get_field('email')._unique = True
User._meta.get_field('email').blank = False
User._meta.get_field('email').null = False

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100 )
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class UserProfile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    profileimage = models.CharField(default='False', max_length=200)
    bio = models.CharField(max_length=250)
    def __str__(self):
        return self.user.username        

class Blog(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now= True)
    description = models.TextField()
    imageurl = models.CharField(default='False', max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-updated_on']

    def __str__(self):
        return self.title        
 
class Event(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='event_posts')
    updated_on = models.DateTimeField(auto_now= True)
    description = models.TextField()
    imageurl = models.CharField(default='False', max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)
    event_on = models.DateTimeField()
    tag = models.CharField(max_length=15)
    class Meta:
        ordering = ['-event_on']

    def __str__(self):
        return self.title        
  