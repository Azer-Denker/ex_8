from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import make_naive
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, FormView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy

from webapp.models import Project, Tipe
from webapp.forms import ProjectForm, BROWSER_DATETIME_FORMAT, ProjectDeleteForm


class PIndexView(ListView):
    template_name = 'project/index.html'
    model = Project
    context_object_name = 'projects'


class ProjectView(DetailView):
    template_name = 'project/view.html'
    model = Project


class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project/create.html'

    def get_success_url(self):
        return reverse('project_view', kwargs={'pk': self.object.pk})


class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project/update.html'

    def get_success_url(self):
        return reverse('project_view', kwargs={'pk': self.object.pk})


class ProjectDeleteView(DeleteView):
    template_name = 'project/delete.html'
    model = Project
    context_object_name = 'project'
    success_url = reverse_lazy('projects')
