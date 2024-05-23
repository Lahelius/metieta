from django.shortcuts import render, redirect
from .models import Project, Task, Client, Team, TeamMember
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
import datetime

from django.core.paginator import Paginator

# Create your views here.
class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('teams')

def logout_user(request):
    logout(request)
    return redirect('login')

class ProjectCreate(LoginRequiredMixin,CreateView):
    model = Project
    fields = '__all__'
    context_object_name = 'project'

class ProjectUpdate(LoginRequiredMixin, UpdateView):
    model = Project
    fields = ['title', 'description', 'deadline', 'complete']
    success_url = reverse_lazy('projects')

class ProjectDelete(LoginRequiredMixin, DeleteView):
    model = Project
    context_object_name = 'project'
    success_url = reverse_lazy('projects')

#For the purposes of this project, the TaskList can be treated as the ProjectDetail
class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'base/task_list.html'

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        return Task.objects.filter(project_id=project_id)
    
    
class Register(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('projects')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(Register, self).form_valid(form)


@login_required(login_url='/login/')
def project_detail(request, pk):
    project = Project.objects.get(id=pk)
    tasks = Task.objects.filter(project_id=pk)
    return render(request, 'base/project_detail.html', {'project': project, 'tasks': tasks})

@login_required(login_url='/login/')
def client_list(request,pk):
    client_list = Client.objects.all().filter(team=pk)
    team_name = Team.objects.get(id=pk).name
    context = {
        'clients': client_list,
        'team' : pk,
        'team_name' : team_name
    }

    return render(request, 'base/client_list.html', context)

@login_required(login_url='/login/')
def project_list(request, pk):
    project_list = Project.objects.all().filter(team=pk).filter(user=request.user.id)
    paginator = Paginator(project_list, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    projects_due_today = project_list.filter(user=request.user.id, deadline=datetime.date.today())
    projects_due_next_seven_days = project_list.filter(user=request.user.id, deadline__range=[datetime.date.today(), datetime.date.today() + datetime.timedelta(days=7)])
    projects_due_next_fourteen_days = project_list.filter(user=request.user.id, deadline__range=[datetime.date.today(), datetime.date.today() + datetime.timedelta(days=14)])
    projects_overdue = project_list.filter(user=request.user.id, deadline__lt=datetime.date.today())

    team_name = Team.objects.get(id=pk).name

    context = {
        'projects': project_list,
        'page_obj': page_obj,
        'num_due_today': len(projects_due_today),
        'num_due_next_seven_days': len(projects_due_next_seven_days),
        'num_due_next_fourteen_days': len(projects_due_next_fourteen_days),
        'num_overdue': len(projects_overdue),
        'team' : pk,
        'team_name' : team_name
    }
    
    return render(request, 'base/project_list.html', context)

@login_required(login_url='/login/')
def team_list(request):
    user_id = request.user.id
    
    team_ids = TeamMember.objects.values('team').filter(user_id=user_id)
    teams = Team.objects.all().filter(id__in=team_ids)

    my_teams = Team.objects.all().filter(owner=user_id)

    shared_teams = teams.exclude(id__in=my_teams.values('id'))

    context = {
        'teams': teams,
        'my_teams': my_teams,
        'shared_teams': shared_teams
    }

    return render(request, 'base/team_list.html', context)
