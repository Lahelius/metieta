from django.contrib import admin
from .models import Client, Project, Task, Team, TeamMember

# Register your models here.
admin.site.register(Client)
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Team)
admin.site.register(TeamMember)   