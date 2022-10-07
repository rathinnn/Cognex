"""ProjectManagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from users import views as userviews
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', userviews.index, name = 'home'),
    path('register', userviews.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('main/', userviews.main, name='main'),
    path('Task/create/<int:pk>', userviews.createTask, name='createTask'),
    path('Project/create', userviews.createProject, name='createProject'),
    path('Project/<pk>/', userviews.ProjectDetailView.as_view(), name = "projectview"),
    path('Project/<int:p_id>/Task/<int:pk>', userviews.taskcompleted, name='taskcompleted'),
    path('Project/User/complete/<int:pk>', userviews.projectcompleted, name='projectcompleted'),
    path('accept/<int:pk>', userviews.acceptTask, name='accept'),
    path('reject/<int:pk>', userviews.rejectTask, name='reject')
]
