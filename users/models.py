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
    
