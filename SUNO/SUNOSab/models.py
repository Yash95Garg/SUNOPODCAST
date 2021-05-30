from django.db import models

# Create your models here.

class Register(models.Model):
    UserID = models.AutoField(primary_key=True)
    Username = models.CharField(max_length=50)
    Email = models.EmailField(max_length=50)
    Password = models.CharField(max_length=50)

    