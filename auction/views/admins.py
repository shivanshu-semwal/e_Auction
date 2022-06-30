from django.shortcuts import render
from django.views.generic import (View, TemplateView,
                                  ListView, DetailView,
                                  CreateView, UpdateView,
                                  DeleteView)
from django.utils.decorators import method_decorator
from auction import models
from django.urls import reverse


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

class CategoriesListView(ListView):
    context_object_name = 'categories'
    model = models.Category
    template_name = 'admins/categories.html'

class CategoriesDetailView(DetailView):
    context_object_name = 'category'
    model = models.Category
    template_name = 'admins/category/detail.html'

class CategoriesCreateView(CreateView):
    fields = "__all__"
    model = models.Category
    template_name = 'admins/category/add.html'

    def get_absolute_url(self):
        return reverse('categories')