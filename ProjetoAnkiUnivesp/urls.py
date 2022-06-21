"""ProjetoAnkiUnivesp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.generic.base import View
from core import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    url(r'^$', views.index, name="index"),     
    url(r'^contato/$', views.contact, name="contact"),
    url(r'^entrar/$', LoginView.as_view(template_name='login.html'), name='login'), 
    url(r'^sair/$', LogoutView.as_view(next_page = 'index'), name='logout'),  
    url(r'^ajuda/$', views.help, name="help"),
    url(r'^arquivo/$', views.file, name="file"), 
    url(r'^projeto/$', views.project, name="project"),
    url(r'^config_tentativa/$', views.create_attempt, name="config_tentativa"),
    url(r'^tentativa/$', views.list_attempt, name="list_attempt"),
    url(r'^conta/', include('accounts.urls', namespace='accounts')),
    url(r'^questoes/', include('core.urls', namespace='core')),   
    # url(r'^questoes/$', views.list_question, name="list_question"),   
    url(r'^materias/$', views.list_theme, name="list_theme"),   
    url(r'^admin/', admin.site.urls),
    #teste
    url(r'^readText/$',views.readText, name="readText"),
    
]
