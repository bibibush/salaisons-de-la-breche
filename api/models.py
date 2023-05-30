from django.db import models
from users.models import Users
# Create your models here.


class Order(models.Model):
    name = models.CharField(max_length=50, null=True)
    adresse = models.CharField(max_length=50, null=True)
    user = models.ForeignKey(Users,on_delete=models.CASCADE, null=True)
    order_list = models.JSONField( null=True)

    def __str__(self):
        return self.name

class File(models.Model):
    title = models.CharField(max_length=30, null=True)
    file = models.FileField(null=True)

    def __str__(self):
        return self.file.name