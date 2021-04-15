from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
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


class ProjectCreateView(PermissionRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project/create.html'
    permission_required = 'webapp.add_project'

    def get_success_url(self):
        return reverse('project_view', kwargs={'pk': self.object.pk})


class ProjectUpdateView(PermissionRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project/update.html'
    permission_required = 'webapp.change_project'

    def get_success_url(self):
        return reverse('project_view', kwargs={'pk': self.object.pk})


class ProjectDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'project/delete.html'
    model = Project
    context_object_name = 'project'
    success_url = reverse_lazy('projects')
    permission_required = 'webapp.delete_project'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = super().get_success_url()

        self.object.is_deleted = True
        self.object.save()
        return HttpResponseRedirect(success_url)
