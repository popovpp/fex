from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from account.managers import CustomUserManager
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
import django.utils.timezone


#class User_old(AbstractUser):
#    username = None
#    email = models.EmailField(_('email address'), unique=True)
#    balance = models.PositiveIntegerField(default=0)
#    freeze_balance = models.PositiveIntegerField(default=0)

#    USERNAME_FIELD = 'email'
#    REQUIRED_FIELDS = []

#    objects = CustomUserManager()

#    def __str__(self):
#        return self.email


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True, max_length=254)
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    password = models.CharField(max_length=128, verbose_name='password')
    last_login = models.DateTimeField(blank=True, null=True, verbose_name='last login')
    is_superuser = models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')
    first_name = models.CharField(blank=True, max_length=30, verbose_name='first name')
    last_name = models.CharField(blank=True, max_length=150, verbose_name='last name')
    is_staff = models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')
    is_active = models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')
    date_joined = models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')
    balance = models.PositiveIntegerField(default=0)
    freeze_balance = models.PositiveIntegerField(default=0)
    groups = models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
