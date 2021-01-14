from django.db import models

# Create your models here.
#from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager

from django.conf import settings


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    balance = models.IntegerField()
    freeze_balanca = models.IntegerField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email