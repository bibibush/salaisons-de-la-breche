from django.db import models
from users.models import Users
# Create your models here.


class Order(models.Model):
    name = models.CharField(max_length=50, null=True)
    adresse = models.CharField(max_length=50, null=True)
    phonenumber = models.CharField(max_length=50, null=True)
    entreprise = models.CharField(max_length=100, null=True)
    user = models.ForeignKey(Users,on_delete=models.CASCADE, null=True, blank=True)
    email = models.CharField(max_length=50, null=True)
    order_file = models.FileField(null=True)
    
    def __str__(self):
        return self.name

class File(models.Model):
    title = models.CharField(max_length=30, null=True)
    file = models.FileField(null=True)

    def __str__(self):
        return self.file.name