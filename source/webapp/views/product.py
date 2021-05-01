from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy

from webapp.models import Product, Review
from webapp.forms import ProductForm


class PIndexView(ListView):
    template_name = 'product/index.html'
    model = Product
    context_object_name = 'products'


class ProductView(DetailView):
    template_name = 'product/view.html'
    model = Product
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        reviews = Review.objects
        kwargs['reviews'] = reviews
        if not self.request.user.groups.filter(name='Moderators'):
            kwargs['reviews'] = kwargs['reviews'].filter(status=True)
        total = 0
        if kwargs['reviews']:
            for review in reviews.all():
                total += review.mark
            total = total / reviews.count()
        kwargs['mark'] = round(total, 1)
        return super().get_context_data(**kwargs)


class ProductCreateView(PermissionRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/create.html'
    permission_required = 'webapp.add_product'

    def get_success_url(self):
        return reverse('product_view', kwargs={'pk': self.object.pk})


class ProductUpdateView(PermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/update.html'
    permission_required = 'webapp.change_product'

    def get_success_url(self):
        return reverse('product_view', kwargs={'pk': self.object.pk})


class ProductDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'product/delete.html'
    model = Product
    context_object_name = 'product'
    success_url = reverse_lazy('products')
    permission_required = 'webapp.delete_product'
