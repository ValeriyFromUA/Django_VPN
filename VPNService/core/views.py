from decimal import Decimal

import requests
from bs4 import BeautifulSoup
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView

from core.forms import NewGuestForm
from core.models import Guest, Portals
from core.utils import get_domain_from_url, modify_links


class HomeView(View):
    template_name = "home.html"

    def get(self, request):
        form = NewGuestForm()
        return render(request, self.template_name)


class ProxyView(View):

    @staticmethod
    def get(request):
        portals = Portals.objects.filter(guest=request.user)
        return render(request, 'proxy.html', {'portals': portals})

    @staticmethod
    def post(request):
        website = request.POST.get("website")
        portal_name = request.POST.get("portal_name")
        portal = Portals(
            guest=request.user,
            portal_name=portal_name,
            domain=get_domain_from_url(website),
        )
        portal.save()

        return redirect(reverse('proxy_more', args=[website]))


class ProxyMoreView(View):

    @staticmethod
    def get(request, website, path=None):
        data = requests.get(website)
        domain = get_domain_from_url(website)
        portal = get_object_or_404(Portals, domain=domain)
        soup = BeautifulSoup(data.content, 'lxml')
        data_size_mb = Decimal(len(data.content)) / Decimal(1024 * 1024)
        portal.data_volume += data_size_mb
        portal.save()

        modify_links(soup, domain)
        html_content = soup.prettify()
        return render(request, 'proxy_view.html', {'html_content': html_content})


class RegistrationView(View):
    @staticmethod
    def get(request):
        form = NewGuestForm()
        return render(request, "registration.html", {"form": form})

    @staticmethod
    def post(request):
        form = NewGuestForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("profile", args=[str(user.pk)]))
        else:
            if "email" in form.errors:
                messages.error(request, "Invalid email address")
            if "username" in form.errors:
                messages.error(request, "Invalid phone")
            if "password1" in form.errors:
                messages.error(request, "Invalid password")
            if "password2" in form.errors:
                messages.error(request, "Passwords do not match")

        return render(request, "registration.html", {"form": form})


class LoginView(View):
    @staticmethod
    def get(request):
        return render(request, "login.html")

    @staticmethod
    def post(request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "Username OR password does not exist")
            return render(request, "login.html")

        login(request, user)
        return redirect(reverse("profile", args=[user.id]))


class LogoutView(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        logout(request)
        return redirect(reverse_lazy("login"))


class GuestProfileView(LoginRequiredMixin, DetailView):
    model = Guest
    template_name = "profile.html"
    context_object_name = "guest"
