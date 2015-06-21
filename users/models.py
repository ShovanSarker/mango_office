from django.db import models
from status.models import Status
# Create your models here.


class AllUsers(models.Model):
    username = models.CharField(max_length=24, null=True, blank=True)
    Name = models.CharField(max_length=24, null=True, blank=True)
    Email = models.EmailField()
    Designation = models.CharField(max_length=24, null=True, blank=True)
    Phone = models.CharField(max_length=15, null=True, blank=True)
    Active = models.BooleanField(default=True)
    Status = models.ForeignKey(Status, related_name='user status')
    DateAdded = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.username


class ACL(models.Model):
    user = models.OneToOneField(AllUsers, primary_key=True)
    CanSeeOthersTaskList = models.BooleanField(default=False)
    CanSeeOthersAttendance = models.BooleanField(default=False)
    CanAddMoreEmployee = models.BooleanField(default=False)
    CanSeeOthersDetails = models.BooleanField(default=False)
    CanAddMoreStatus = models.BooleanField(default=False)
    CanSeeOthersStatus = models.BooleanField(default=False)
    DateAdded = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.user
