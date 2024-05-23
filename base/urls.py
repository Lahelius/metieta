from django.urls import path
from .views import CustomLoginView, logout_user, client_list, team_list, project_list
from .views import ProjectCreate, project_detail, Register

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', Register.as_view(), name='register'),
    path('',team_list, name='teams'),
    path('team/<int:pk>/', project_list, name='projects'),
    path('team/<int:pk>/clients/', client_list, name='clients'),
    path('project/<int:pk>/', project_detail, name='project-detail'),
    path('project-create/', ProjectCreate.as_view(), name='project-create')
]