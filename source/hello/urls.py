"""hello URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from webapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', PIndexView.as_view(), name='projects'),
    path('projects/add/', ProjectCreateView.as_view(), name='project_create'),
    path('project/<int:pk>/', ProjectView.as_view(), name='project_view'),
    path('project/<int:pk>/update/', ProjectUpdateView.as_view(), name='project_update'),
    # # path('project/<int:pk>/delete/', project_delete_view, name='project_delete'),
    path('project/<int:pk>/tipes', TIndexView.as_view(), name='tipes'),
    path('project/<int:pk>/tipes/add/', TipeCreateView.as_view(), name='tipe_create'),
    path('tipe/<int:pk>/', TipeView.as_view(), name='tipe_view'),
    path('tipe/<int:pk>/update/', TipeUpdateView.as_view(), name='tipe_update'),
    path('tipe/<int:pk>/delete/', tipe_delete_view, name='tipe_delete'),
]
