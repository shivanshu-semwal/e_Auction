from django.shortcuts import render
from django.views.generic import (View, TemplateView,
                                  ListView, DetailView,
                                  CreateView, UpdateView,
                                  DeleteView)
from django.utils.decorators import method_decorator
from auction import models
from django.urls import reverse
from django import forms


class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'


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
              'image', 'start_time', 'end_time')
    model = models.Product
    template_name = 'seller/product/add.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['start_time'].widget = DateTimeInput()
        context['form'].fields['end_time'].widget = DateTimeInput()
        return context
