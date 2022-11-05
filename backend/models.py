from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import *

# On instancie ici un model salarié qui serat les utilisateurs de l'app
class Salarie(AbstractUser):
    username = None
    email = models.EmailField('email', unique=True)
    role  = models.CharField('role', default='salarié', max_length=50)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = SalarieManager()

    def __str__(self):
        return self.email

