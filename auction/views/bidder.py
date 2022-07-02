from turtle import update
from django.forms import Form
from django.shortcuts import render
from django.views.generic import (View, TemplateView,
                                  ListView, DetailView,
                                  CreateView, UpdateView,
                                  DeleteView)
from django.utils.decorators import method_decorator
from auction import models
from django.urls import reverse, reverse_lazy
from django.db.models import Q

def bidder_home(request):
    return render(request, 'bidder/home.html')


def bidder_profile(request):
    seller = models.Bidder(request.user)
    return render(
        request,
        'bidder/profile.html',
        {
            'seller': seller
        }
    )


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
            auctioned_product = models.AuctionedProduct.objects.get(
                pk=self.object.product.auctioned.pk)
            auctioned_product.amount = self.object.amount
            auctioned_product.bidder = self.object.bidder
            auctioned_product.save()
        self.object.save()
        return super().form_valid(form)


class BidListView(ListView):
    model = models.Bid
    template_name = 'bidder/bids.html'
    context_object_name = 'bids'

    def get_queryset(self):
        return self.model.objects.filter(bidder=self.request.user.bidder)


class ProductListView(ListView):
    model = models.Product
    template_name = 'bidder/products.html'
    context_object_name = 'products'

    def get_queryset(self):
        products = models.Product.objects.all()
        for product in products:
            a = product.getStatus
        return self.model.objects.filter(status__isnull=True)

class ProductDetailView(DetailView):
    model = models.Product
    template_name = 'bidder/products/detail.html'
    context_object_name = 'product'