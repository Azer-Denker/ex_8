from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotAllowed, HttpResponseNotFound
from django.urls import reverse, reverse_lazy
from django.utils.timezone import make_naive
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView, DeleteView

from webapp.models import Tipe, Project
from webapp.forms import TipeForm, BROWSER_DATETIME_FORMAT, SimpleSearchForm


class TIndexView(ListView):
    template_name = 'tipe/index.html'
    context_object_name = 'tipes'
    model = Tipe
    paginate_by = 5
    paginate_orphans = 0

    def get_context_data(self, *, object_list=None, **kwargs):
        form = SimpleSearchForm(data=self.request.GET)
        if form.is_valid():
            search = form.cleaned_data['search']
            kwargs['search'] = search
        return super().get_context_data(object_list=object_list, **kwargs)

    def get_queryset(self):
        data = Tipe.objects.all()
        form = SimpleSearchForm(data=self.request.GET)
        if form.is_valid():
            search = form.cleaned_data['search']
            if search:
                data = data.filter(Q(title__icontains=search) | Q(text__icontains=search))

        return data.order_by('-created_at')


class TipeView(DetailView):
    template_name = 'tipe/view.html'
    model = Tipe
    template_name_field = "tipe"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.project_pk.is_deleted:
            return HttpResponseNotFound()

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     tipe = self.object
    #     project = tipe.project_pk.start_date('-start_date')
    #     context['project'] = project
    #     return context


class TipeCreateView(CreateView):
    model = Tipe
    template_name = 'tipe/create.html'
    form_class = TipeForm

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        tipe = form.save(commit=False)
        tipe.project_pk = project
        tipe.save()
        form.save_m2m()
        return redirect('tipe_view', pk=tipe.pk)


class TipeUpdateView(UpdateView):
    template_name = 'tipe/update.html'
    form_class = TipeForm
    model = Tipe

    def get_success_url(self):
        return reverse('tipe_view', kwargs={'pk': self.object.pk})


class TipeDeleteView(DeleteView):
    template_name = 'tipe/delete.html'
    model = Tipe
    context_key = 'tipe'

    def get_success_url(self):
        return reverse('project_view', kwargs={'pk': self.object.project_pk.pk})

