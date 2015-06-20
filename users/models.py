from django.db import models

# Create your models here.


class AllUsers(models.Model):
    username = models.CharField(max_length=24, null=True, blank=True)
    Name = models.CharField(max_length=24, null=True, blank=True)
    Email = models.EmailField()
    Designation = models.CharField(max_length=24, null=True, blank=True)
    Phone = models.CharField(max_length=15, null=True, blank=True)
    Admin = models.BooleanField(default=False)
    Active = models.BooleanField(default=True)
    DateAdded = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.username
