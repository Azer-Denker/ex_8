from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DeleteView

from webapp.models import Review, Product
from webapp.forms import ReviewForm


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    template_name = 'review/create.html'
    form_class = ReviewForm

    def form_valid(self, form):
        product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        review = form.save(commit=False)
        review.product = product
        review.author = self.request.user
        if not self.request.user.groups.filter(name='Moderators'):
            review.status = False
        else:
            review.status = True
        review.save()
        form.save_m2m()
        return redirect('product_view', pk=product.pk)


class ReviewUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'review/update.html'
    form_class = ReviewForm
    model = Review
    permission_required = 'webapp.change_review'

    def has_permission(self):
        review = self.get_object()
        return super().has_permission() or review.author == self.request.user

    def get_success_url(self):
        return reverse('product_view', kwargs={'pk': self.object.product.pk})


class ReviewDeleteView(PermissionRequiredMixin, DeleteView):
    model = Review
    permission_required = 'webapp.delete_review'

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def has_permission(self):
        review = self.get_object()
        return super().has_permission() or review.author == self.request.user

    def get_success_url(self):
        return reverse('product_view', kwargs={'pk': self.object.product.pk})
