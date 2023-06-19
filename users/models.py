from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Users(AbstractUser):
    username = models.CharField(max_length=50, blank=True, unique=True, null=True)
    nom = models.CharField(max_length=20, null=True)
    prenom = models.CharField(max_length=20, null=True)
    entreprise = models.CharField(max_length=30, null=True)
    phonenumber = models.CharField(max_length=20, null=True)
    adresse = models.CharField(max_length=50, null=True)

    USERNAME_FIELD = 'username'
