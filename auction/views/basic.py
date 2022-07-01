from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

from auction.decorators import unauthenticated_user


def index(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        group = request.user.groups.all()[0].name
        if group == 'sellers':
            return HttpResponseRedirect(reverse('seller_home'))
        elif group == 'bidders':
            return HttpResponseRedirect(reverse('bidder_home'))
        elif group == 'admins':
            return HttpResponseRedirect(reverse('admin_home'))
        else:
            return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'auction/index.html')


def about_us(request):
    return render(request, 'auction/about.html')


@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@unauthenticated_user
def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                group = user.groups.all()[0].name
                if group == 'users':
                    return HttpResponseRedirect(reverse('index'))
                elif group == 'bidders':
                    return HttpResponseRedirect(reverse('bidder_home'))
                elif group == 'admins':
                    return HttpResponseRedirect(reverse('admin_home'))
                else:
                    return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Account not active!")
        else:
            print('someone try to login!!!')
            return render(request, 'auction/login.html', {})
    else:
        print("(debug) inside login user view")
        return render(request, 'auction/login.html', {})
