from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Users(AbstractUser):
    phonenumber = models.CharField(max_length=20, null=True)
    adresse = models.CharField(max_length=50, null=True)
