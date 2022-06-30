from django.shortcuts import render
from django.views.generic import (View, TemplateView,
                                  ListView, DetailView,
                                  CreateView, UpdateView,
                                  DeleteView)
from django.utils.decorators import method_decorator
from auction import models
from django.urls import reverse


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