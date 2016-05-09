from __future__ import unicode_literals


from django.contrib.auth.models import User

from django.db import models


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
