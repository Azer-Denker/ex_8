from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotAllowed, HttpResponseNotFound
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

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_deleted=False)
        return queryset


class ProjectView(DetailView):
    template_name = 'project/view.html'
    model = Project

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_deleted:
            return HttpResponseNotFound()

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project/create.html'

    def get_success_url(self):
        return reverse('project_view', kwargs={'pk': self.object.pk})


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project/update.html'

    def get_success_url(self):
        return reverse('project_view', kwargs={'pk': self.object.pk})


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'project/delete.html'
    model = Project
    context_object_name = 'project'
    success_url = reverse_lazy('projects')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = super().get_success_url()

        self.object.is_deleted = True
        self.object.save()
        return HttpResponseRedirect(success_url)
