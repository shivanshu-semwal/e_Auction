from django.shortcuts import render
from django.views.generic import (View, TemplateView,
                                  ListView, DetailView,
                                  CreateView, UpdateView,
                                  DeleteView)
from django.utils.decorators import method_decorator
from auction.decorators import allowed_users

from auction import models
from django.urls import reverse, reverse_lazy
from django import forms


class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'

class DateInput(forms.DateInput):
    input_type = 'date'


@allowed_users(['sellers'])
def seller_home(request):
    return render(request, 'seller/home.html')


@allowed_users(['sellers'])
def seller_profile(request):
    seller = models.Seller(request.user)
    return render(
        request,
        'seller/profile.html',
        {
            'seller': seller
        }
    )


@method_decorator(allowed_users(['sellers']), name='dispatch')
class ProductListView(ListView):
    context_object_name = 'products'
    model = models.Product
    template_name = 'seller/products.html'

    def get_queryset(self):
        return self.model.objects.filter(creator=self.request.user.seller)


@method_decorator(allowed_users(['sellers']), name='dispatch')
class ProductDetailView(DetailView):
    context_object_name = 'product'
    model = models.Product
    template_name = 'seller/product/view.html'


@method_decorator(allowed_users(['sellers']), name='dispatch')
class ProductCreateView(CreateView):
    fields = ('name', 'description', 'min_price', 'category',
              'image', 'start_time', 'end_time')
    model = models.Product
    template_name = 'seller/product/add.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['start_time'].widget = DateTimeInput()
        context['form'].fields['end_time'].widget = DateTimeInput()
        return context

    def form_valid(self, form):
        form.instance.creator = self.request.user.seller
        auctioned = models.AuctionedProduct(
            bidder=models.User.objects.get(username='default').bidder, amount=form.instance.min_price)
        auctioned.save()
        form.instance.auctioned = auctioned
        return super().form_valid(form)


@method_decorator(allowed_users(['sellers']), name='dispatch')
class ProductUpdateView(UpdateView):
    fields = ('name', 'description', 'min_price',
              'image', 'start_time', 'end_time', 'category')
    model = models.Product
    template_name = 'seller/product/update.html'
    context_object_name = 'product'


@method_decorator(allowed_users(['sellers']), name='dispatch')
class ProductDeleteView(DeleteView):
    model = models.Product
    context_object_name = 'product'
    template_name = 'seller/product/delete.html'
    success_url = reverse_lazy("view_products")


@method_decorator(allowed_users(['sellers']), name='dispatch')
class SellerUpdateProfile(UpdateView):
    model = models.Seller
    fields = ('first_name', 'last_name', 'dob', 'address', 'contact', 'image')
    template_name = 'seller/profile/update.html'
    success_url = reverse_lazy('seller_home')
    context_object_name = 'seller'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['dob'].widget = DateInput()
        return context