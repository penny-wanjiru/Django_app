from __future__ import unicode_literals


from django.contrib.auth.models import User

from django.db import models


class SignUp(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    password_two = models.CharField(max_length=255, default='password')

    def __unicode__(self):
        return u'%s' % self.email


class SignIn(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def __unicode__(self):
        return u'%s' % self.username        


class BucketList(models.Model):
    name = models.CharField(unique=True, max_length=255,
                            default="BucketList")
    date_created = models.DateField(auto_now_add=True, editable=False)
    date_updated = models.DateField(auto_now=True)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return u'%s' % self.name


class BucketListItem(models.Model):
    name = models.CharField(unique=True, max_length=255,
                            default="BucketlistItem")
    date_updated = models.DateField(auto_now=True)
    date_created = models.DateField(auto_now_add=True, editable=False)
    done = models.BooleanField(default=False)
    bucketlist = models.ForeignKey(BucketList, related_name="items")

    def __unicode__(self):
        return u'%s' % self.name
