# from django.http import HttpResponseNotAllowed
# from django.shortcuts import get_object_or_404, redirect, render
# from django.utils.timezone import make_naive
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.urls import reverse

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


# class ProjectUpdateView(FormView):
#     template_name = 'project/update.html'
#     form_class = ProjectForm
#
#     def dispatch(self, request, *args, **kwargs):
#         self.tipe = self.get_object()
#         return super().dispatch(request, *args, **kwargs)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['tipe'] = self.tipe
#         return context
#
#     def get_initial(self):
#         return {'publish_at': make_naive(self.tipe.publish_at)\
#             .strftime(BROWSER_DATETIME_FORMAT)}
#
#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs['instance'] = self.tipe
#         return kwargs
#
#     def form_valid(self, form):
#         self.tipe = form.save()
#         return super().form_valid(form)
#
#     def get_success_url(self):
#         return reverse('tipe_view', kwargs={'pk': self.tipe.pk})
#
#     def get_object(self):
#         pk = self.kwargs.get('pk')
#         return get_object_or_404(Tipe, pk=pk)
#
#
# def project_delete_view(request, pk):
#     project = get_object_or_404(Project, id=pk)
#
#     if request.method == 'GET':
#         form = ProjectDeleteForm
#         return render(request, 'project/delete.html', context={'project': project, 'form': form})
#     elif request.method == 'POST':
#         form = ProjectDeleteForm(data=request.POST)
#         if form.is_valid():
#             if form.cleaned_data['start_date'] != project.start_date:
#                 form.errors['start_date'] = ['Названия проектов не совпадают']
#                 return render(request, 'project/delete.html', context={'project': project, 'form': form})
#
#             project.delete()
#             return redirect('project_list')
#         return render(request, 'project/delete.html', context={'project': project, 'form': form})


# class ProjectTipeCreateView(CreateView):
#     model = Tipe
#     template_name = 'tipe/create.html'
#     form_class = Tipe
#
#     def form_valid(self, form):
#         project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
#         tipe_action = form.save(commit=False)
#         tipe_action.project = project
#         tipe_action.save()
#         form.save_m2m()
#         return redirect('project/view', pk=project.pk)
