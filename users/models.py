import datetime
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Skill(models.TextChoices):
    PYTHON = 'PYTHON'
    JAVA = 'JAVA'
    SCALA = 'SCALA'
    RUST = 'RUST'
    RUBY = 'RUBY'
    PHP = 'PHP'
    JAVASCRIPT = 'JAVASCRIPT'
    CPP = 'CPP'
    C = 'C'

class Project(models.Model):
    title = models.CharField(max_length = 20)
    description = models.TextField(default = '')
    startDate = models.DateField('Project Start Date')
    expectedDate = models.DateField('Estimated Completion Date')
    manager = models.ForeignKey(User,on_delete=models.CASCADE, related_name = 'own_project_set')
    members = models.ManyToManyField(User)
    completed = models.BooleanField(default = False)
    completionDate = models.DateField('Completion Date', default = datetime.date.today)
    

class Task(models.Model):
    class TYPE(models.TextChoices):
        BUG = 'BG', _('BUG')
        FEATURE = 'FT', _('FEATURE')
        REFACTOR = 'RT', _('REFACTOR')
        MIGRATE = 'MG', _('MIGRATE')
    title = models.CharField(max_length = 20)
    description = models.TextField()
    startDate = models.DateField('Task Start Date')
    expectedDate = models.DateField('Estimated Completion Date', default = datetime.date.today)
    weight = models.IntegerField()
    project = models.ForeignKey(Project, on_delete = models.CASCADE)
    completionDate = models.DateField('Completion Date', default = datetime.date.today)
    completed = models.BooleanField(default = False)
    Type = models.CharField(max_length = 2, choices=TYPE.choices, default = TYPE.FEATURE)
    Assigned = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default = False)

class TaskRequest(models.Model):
    project = models.ForeignKey(Project, on_delete = models.CASCADE)
    toUser = models.ForeignKey(User, on_delete = models.CASCADE)
    task = models.ForeignKey(Task, on_delete = models.CASCADE)