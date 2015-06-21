from django.db import models

# Create your models here.


class Status(models.Model):
    Status = models.CharField(max_length=24, null=True, blank=True)
    StatusKey = models.CharField(max_length=24, null=True, blank=True)
    StatusIcon = models.CharField(max_length=64, null=True, blank=True)
    StatusChangeButton = models.CharField(max_length=64, null=True, blank=True)
    DateAdded = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.Status
