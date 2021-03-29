from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotAllowed
from django.urls import reverse
from django.utils.timezone import make_naive
from django.views.generic import ListView, DetailView, FormView, CreateView

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
        return redirect('tipe_view', pk=tipe.pk)


class TipeUpdateView(FormView):
    template_name = 'tipe/update.html'
    form_class = TipeForm

    def dispatch(self, request, *args, **kwargs):
        self.tipe = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipe'] = self.tipe
        return context

    def get_initial(self):
        return {'publish_at': make_naive(self.tipe.publish_at)\
            .strftime(BROWSER_DATETIME_FORMAT)}

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.tipe
        return kwargs

    def form_valid(self, form):
        self.tipe = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tipe_view', kwargs={'pk': self.tipe.pk})

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Tipe, pk=pk)


def tipe_delete_view(request, pk):
    tipe = get_object_or_404(Tipe, pk=pk)
    if request.method == 'GET':
        return render(request, 'tipe/delete.html', context={'tipe': tipe})
    elif request.method == 'POST':
        tipe.delete()
        return redirect('index')
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])
