from django.db import models
import django.utils.timezone
from django.contrib.auth.models import Group
from django.conf import settings

from account.models import User


class Advert(models.Model):

    id = models.AutoField(auto_created=True, primary_key=True, serialize=True,
                          verbose_name='id')
    type_of_advert = tuple([(el.name, el.name)for el in Group.objects.all()])
    type_of_advert = models.CharField(max_length=50, choices=type_of_advert, 
		                              default='', verbose_name='type of advert')
    title = models.CharField(blank=True, max_length=254,
                             verbose_name='Title')
    description = models.TextField(blank=True, verbose_name='Description')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Author')
    status = (('r1', 'new'), ('r2', 'active'), ('r3', 'in_trash'), ('r4', 'completed'))
    status = models.CharField(max_length=2,choices=status, default='r1',
                              verbose_name='status')
    price = models.PositiveIntegerField(default=0, verbose_name='Price')
    deadline = models.DateTimeField(blank=True, null=True,
                                    verbose_name='Deadline')
    created = models.DateTimeField(default=django.utils.timezone.now,
                                   verbose_name='Created')
    updated = models.DateTimeField(auto_now=False, auto_now_add=True,
                                   verbose_name='Updated')
    active_until_date = models.DateTimeField(default=django.utils.timezone.now,
                                   verbose_name='Active until data')

    REQUIRED_FIELDS = []

    class Meta:
    	verbose_name = 'Advert'
    	verbose_name_plural = 'Adverts'

    def __str__(self):
        return self.title


class AdvertFile(models.Model):

    id = models.AutoField(auto_created=True, primary_key=True, serialize=True,
                          verbose_name='ID')
    advert_id = models.ForeignKey(Advert, on_delete=models.CASCADE,
                                  verbose_name='advert_id', default=0)
    advert_file = models.FileField(upload_to=settings.MEDIA_ROOT, default='')

    class Meta:
    	verbose_name = 'AdvertFile'
    	verbose_name_plural = 'AdvertFiles'


    def __str__(self):
        return repr(self.advert_file)


class Reply(models.Model):

    id = models.AutoField(auto_created=True, primary_key=True, serialize=True,
                          verbose_name='id')
    advert_id = models.ForeignKey(Advert, on_delete=models.CASCADE,
                                  verbose_name='advert_id', default=0)
    message = models.TextField(blank=True, verbose_name='Description')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Author')
    planed_date = models.DateTimeField(blank=True, null=True,
                                       verbose_name='Deadline')
    price = models.PositiveIntegerField(default=0, verbose_name='Price')
    

    REQUIRED_FIELDS = []

    class Meta:
    	verbose_name = 'Reply'
    	verbose_name_plural = 'Replies'

    def __str__(self):
        return self.title


class ReplyFile(models.Model):

    id = models.AutoField(auto_created=True, primary_key=True, serialize=True,
                          verbose_name='ID')
    reply_id = models.ForeignKey(Reply, on_delete=models.CASCADE,
                                  verbose_name='reply_id', default=0)
    reply_file = models.FileField(upload_to=settings.MEDIA_ROOT, default='')

    class Meta:
    	verbose_name = 'ReplyFile'
    	verbose_name_plural = 'ReplyFiles'

    def __str__(self):
        return self.reply_file
