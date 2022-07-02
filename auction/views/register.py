from django.shortcuts import render
from django.contrib.auth.models import Group

from auction.forms.register import UserForm, NewSellerForm, NewBidderForm
from auction import views

from auction.decorators import unauthenticated_user

from django.forms import Form
from django.shortcuts import render
from django.views.generic import (
    View, TemplateView,
    ListView, DetailView,
    CreateView, UpdateView,
    DeleteView
)
from django.utils.decorators import method_decorator
from auction import models
from django.urls import reverse, reverse_lazy
from django.db.models import Q


@unauthenticated_user
def register(request):
    return render(request, 'auction/register.html')


@unauthenticated_user
def create_auction_seller(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        auction_user_form = NewSellerForm(
            data=request.POST, files=request.FILES)
        if user_form.is_valid() and auction_user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            auction_user = auction_user_form.save(commit=False)
            auction_user.user = user
            if 'image' in request.FILES:
                auction_user.image = request.FILES['image']
            auction_user.save()
            registered = True
            # goto the index page
            Group.objects.get(name='sellers').user_set.add(user)
            return views.basic.index(request)
        else:
            print('error form invalid')
    else:
        user_form = UserForm()
        auction_user_form = NewSellerForm()
    return render(
        request,
        'auction/register/user.html',
        {
            'user_form': user_form,
            'auction_user_form': auction_user_form,
            'registered': registered
        }
    )


@unauthenticated_user
def create_auction_bidder(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        bidder_form = NewBidderForm(data=request.POST, files=request.FILES)
        if user_form.is_valid() and bidder_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            bidder = bidder_form.save(commit=False)
            bidder.user = user
            if 'image' in request.FILES:
                bidder.image = request.FILES['image']
            bidder.save()
            registered = True
            # goto the index page
            Group.objects.get(name='bidders').user_set.add(user)
            return views.basic.index(request)
        else:
            print('User Form:')
            print(user_form.errors)
            print('Bidder Form:')
            print(bidder_form.errors)
    else:
        user_form = UserForm()
        bidder_form = NewBidderForm()

    return render(
        request,
        'auction/register/bidder.html',
        {
            'user_form': user_form,
            'bidder_form': bidder_form,
            'registered': registered
        }
    )


@unauthenticated_user
def create_auction_admin(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
            Group.objects.get(name='admins').user_set.add(user)
            return views.basic.index(request)
        else:
            print('User Form:')
            print(user_form.errors)
    else:
        user_form = UserForm()
    return render(
        request,
        'auction/register/admin.html',
        {
            'user_form': user_form,
            'registered': registered
        }
    )
