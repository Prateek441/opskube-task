from django.db import models
# Create your models here.

class Seller(models.Model):
    name= models.CharField(max_length=50)
    email= models.EmailField(unique=True)
    phone= models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=200)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.email