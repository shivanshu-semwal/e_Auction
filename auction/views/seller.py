from django.shortcuts import render
from django.views.generic import (View, TemplateView,
                                  ListView, DetailView,
                                  CreateView, UpdateView,
                                  DeleteView)
from django.utils.decorators import method_decorator
from auction import models
from django.urls import reverse


def seller_home(request):
    return render(request, 'seller/home.html')


def seller_profile(request):
    seller = models.Seller(request.user)
    return render(
        request,
        'seller/profile.html',
        {
            'seller': seller
        }
    )


class ProductListView(ListView):
    context_object_name = 'products'
    model = models.Product
    template_name = 'seller/products.html'


class ProductDetailView(DetailView):
    context_object_name = 'product'
    model = models.Product
    template_name = 'seller/product/view.html'


class ProductCreateView(CreateView):
    fields = ('name', 'description', 'min_price',
              'images', 'session', 'category')
    model = models.Product
    template_name = 'seller/product/add.html'

    def get_absolute_url(self):
        return reverse('sellers/product/view', kwargs={'pk': self.pk})
