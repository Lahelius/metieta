from django.db import models
from django.contrib.auth.models import User

# Create your models here
class Team(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length = 256, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

class Client(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length = 256, null=False, blank=True)
    contact_name = models.CharField(max_length = 256, null=True, blank=True)
    contact_email = models.EmailField(null=True, blank=True)
    contact_phone = models.CharField(max_length = 256, null=True, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-active','name']

class Project(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user')
    manager = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='manager')
    title = models.CharField(max_length = 256, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField(null=True, blank=True)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return "{" + self.user.__str__() + "," + self.deadline.__str__()+ "," + self.title.__str__() + "}"

    class Meta:
        ordering = ['deadline', 'title']

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length = 256, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    
    def __str__(self):
        return "{" + self.project.__str__() + "," + self.title.__str__() +"}"
    
    class Meta:
        ordering = ['complete']