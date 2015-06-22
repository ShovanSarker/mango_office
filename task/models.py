from django.db import models
from users.models import AllUsers

# Create your models here.

class Task(models.Model):
    Task = models.CharField(max_length=32, null=True, blank=True)
    AssignedBy = models.ForeignKey(AllUsers, related_name='who have given')
    AssignedTo = models.ForeignKey(AllUsers, related_name='who was given')
    Deadline = models.DateField(null=True, blank=True)
    Description = models.TextField(null=True, blank=True)
    Complete = models.BooleanField(default=False)
    Remarks = models.CharField(max_length=32, null=True, blank=True)
    DateAdded = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.Task
