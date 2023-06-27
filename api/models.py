from django.db import models
from users.models import Users
# Create your models here.


class Order(models.Model):
    nom = models.CharField(max_length=50, null=True)
    prenom = models.CharField(max_length=50, null=True)
    adresse = models.CharField(max_length=50, null=True)
    phonenumber = models.CharField(max_length=50, null=True)
    entreprise = models.CharField(max_length=100, null=True)
    user = models.ForeignKey(Users,on_delete=models.CASCADE, blank=True, null=True)
    email = models.CharField(max_length=50, null=True)
    create_dt = models.DateField(auto_now_add=True, null=True)
    modify_dt = models.DateField(auto_now=True)
    order_file = models.FileField(upload_to='upload/', null=True)
    order_number = models.CharField(max_length=10, blank=True, null=True)
    date = models.DateField(null=True)
    pay = models.BooleanField(default=False)
    block = models.BooleanField(default=False)
    
    def __str__(self):
        return self.nom

class File(models.Model):
    title = models.CharField(max_length=30, null=True)
    file = models.FileField(null=True)

    def __str__(self):
        return self.title