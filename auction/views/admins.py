from django.shortcuts import render
from django.views.generic import (View, TemplateView,
                                  ListView, DetailView,
                                  CreateView, UpdateView,
                                  DeleteView)
from django.utils.decorators import method_decorator
from auction import models
from django.urls import reverse_lazy


from django.utils.decorators import method_decorator
from auction.decorators import allowed_users
# @method_decorator(allowed_users(['admins']), name='dispatch')


@allowed_users(['admins'])
def admin_profile(request):
    user = request.user
    return render(request, 'admins/profile.html')


@allowed_users(['admins'])
def admin_home(request):
    return render(request, 'admins/home.html')


@method_decorator(allowed_users(['admins']), name='dispatch')
class CategoriesListView(ListView):
    context_object_name = 'categories'
    model = models.Category
    template_name = 'admins/categories.html'


@method_decorator(allowed_users(['admins']), name='dispatch')
class CategoriesDetailView(DetailView):
    context_object_name = 'category'
    model = models.Category
    template_name = 'admins/category/detail.html'


@method_decorator(allowed_users(['admins']), name='dispatch')
class CategoriesCreateView(CreateView):
    fields = "__all__"
    model = models.Category
    template_name = 'admins/category/add.html'


@method_decorator(allowed_users(['admins']), name='dispatch')
class CategoriesUpdateView(UpdateView):
    fields = ('name', 'description')
    model = models.Category
    template_name = 'admins/category/update.html'


@method_decorator(allowed_users(['admins']), name='dispatch')
class CategoriesDeleteView(DeleteView):
    model = models.Category
    template_name = 'admins/category/delete.html'
    success_url = reverse_lazy("view_categories")


@method_decorator(allowed_users(['admins']), name='dispatch')
class ProductListView(ListView):
    model = models.Product
    template_name = 'admins/products.html'
    context_object_name = 'products'

@method_decorator(allowed_users(['admins']), name='dispatch')
class ProductDetailView(DetailView):
    model = models.Product
    template_name = 'admins/product/view.html'
    context_object_name = 'product'

@method_decorator(allowed_users(['admins']), name='dispatch')
class ReportCreateView(CreateView):
    fields = ('title', 'description')
    model = models.Report
    template_name = 'admins/report/add.html'
    success_url = reverse_lazy('admin_home')

    def form_valid(self, form):
        form.instance.product = models.Product.objects.get(pk=self.kwargs['product_pk'])
        return super().form_valid(form)