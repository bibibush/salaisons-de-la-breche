from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Users(AbstractUser):
    email = models.EmailField(_('email adress'), unique=True)
    entreprise = models.CharField(max_length=30)
    phonenumber = models.CharField(max_length=20)
    adresse = models.CharField(max_length=50)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS= ['username']

    def __str__(self):
        return self.username
    
class Contact(models.Model):
    nom = models.CharField(max_length=30)
    prenom = models.CharField(max_length=30)
    number = models.CharField(max_length=30)
    email = models.EmailField(max_length=100)
    create_dt = models.DateTimeField(auto_now_add=True)
    sujet = models.CharField(max_length=250, null=True, blank=True)
    question = models.TextField()

    def __str__(self):
        return self.nom