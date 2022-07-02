from django.forms import Form
from django.shortcuts import render
from django.views.generic import (
    View, TemplateView,
    ListView, DetailView,
    CreateView, UpdateView,
    DeleteView
)
from django.utils.decorators import method_decorator
from auction.decorators import allowed_users

from auction import models
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django import forms

class DateInput(forms.DateInput):
    input_type = 'date'

@allowed_users(['bidders'])
def bidder_home(request):
    return render(request, 'bidder/home.html')


@allowed_users(['bidders'])
def bidder_profile(request):
    seller = models.Bidder(request.user)
    return render(
        request,
        'bidder/profile.html',
        {
            'seller': seller
        }
    )


@method_decorator(allowed_users(['bidders']), name='dispatch')
class BidCreateView(CreateView):
    fields = ('amount',)
    model = models.Bid
    template_name = 'bidder/bid/create.html'
    success_url = reverse_lazy('bidder_home')

    def form_valid(self, form):
        product = models.Product.objects.get(pk=self.kwargs['product_pk'])
        if self.request.user.bidder == product.auctioned.bidder:
            form.add_error(field='amount', error='Your bid is the highest!!')
            return super().form_invalid(form)
        self.object = form.save(commit=False)
        self.object.product = product
        self.object.bidder = self.request.user.bidder
        if self.object.amount <= self.object.product.auctioned.amount:
            form.add_error(field='amount', error='Bid Higher!!')
            return super().form_invalid(form)
        else:
            # fail his old bids
            models.UPDATE_REF = "ref1"
            bids = models.Bid.objects.filter(
                bidder=self.object.bidder, product=self.object.product)
            for bid in bids:
                # add balance back
                bidder = models.Bidder.objects.get(pk=bid.bidder.pk)
                bidder.balance = bidder.balance + bid.amount
                bidder.save()
                bid.status = "FAIL"
                bid.save()
            if self.object.amount > self.object.bidder.balance:
                form.add_error(
                    field='amount', error='Your account balance is less!!')
                return super().form_invalid(form)
            bidder = models.Bidder.objects.get(pk=self.object.bidder.pk)
            bidder.balance =  bidder.balance - self.object.amount
            bidder.save()
            auctioned_product = models.AuctionedProduct.objects.get(
                pk=self.object.product.auctioned.pk)
            auctioned_product.amount = self.object.amount
            auctioned_product.bidder = self.object.bidder
            auctioned_product.save()
        self.object.save()
        return super().form_valid(form)


@method_decorator(allowed_users(['bidders']), name='dispatch')
class BidListView(ListView):
    model = models.Bid
    template_name = 'bidder/bids.html'
    context_object_name = 'bids'

    def get_queryset(self):
        return self.model.objects.filter(bidder=self.request.user.bidder)


@method_decorator(allowed_users(['bidders']), name='dispatch')
class ProductListView(ListView):
    model = models.Product
    template_name = 'bidder/products.html'
    context_object_name = 'products'

    def get_queryset(self):
        products = models.Product.objects.all()
        for product in products:
            a = product.getStatus
        return self.model.objects.filter(status__isnull=True)


@method_decorator(allowed_users(['bidders']), name='dispatch')
class ProductDetailView(DetailView):
    model = models.Product
    template_name = 'bidder/product/view.html'
    context_object_name = 'product'


@method_decorator(allowed_users(['bidders']), name='dispatch')
class BidderUpdateProfile(UpdateView):
    model = models.Bidder
    fields = ('first_name', 'last_name', 'dob', 'address', 'contact', 'image')
    template_name = 'bidder/profile/update.html'
    success_url = reverse_lazy('bidder_home')
    context_object_name = 'bidder'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['dob'].widget = DateInput()
        return context


@method_decorator(allowed_users(['bidders']), name='dispatch')
class ItemsListView(ListView):
    model = models.AuctionedProduct
    template_name = 'bidder/items.html'
    context_object_name = 'products'

    def get_queryset(self):
        products = models.Product.objects.all()
        for product in products:
            a = product.getStatus
        return self.model.objects.filter(bidder=self.request.user.bidder)
