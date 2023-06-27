from django.db import models
from users.models import Users
# Create your models here.


class Order(models.Model):
    nom = models.CharField('nom',max_length=50)
    prenom = models.CharField('prenom',max_length=50)
    adresse = models.CharField('adresse',max_length=50)
    phonenumber = models.CharField('phonenumber',max_length=50)
    entreprise = models.CharField('entreprise',max_length=100)
    user = models.ForeignKey(Users,on_delete=models.CASCADE, blank=True, null=True)
    email = models.CharField('email',max_length=50)
    create_dt = models.DateTimeField('create date',auto_now_add=True)
    modify_dt = models.DateField('modify date',auto_now=True)
    order_file = models.FileField(upload_to='upload/', null=True)
    order_number = models.CharField('order number',max_length=10, blank=True)
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