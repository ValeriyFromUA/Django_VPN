from decimal import Decimal

import requests
from bs4 import BeautifulSoup
from core.forms import NewGuestForm
from core.models import Portals
from core.utils import get_domain_from_url, modify_links
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView


@method_decorator(login_required, name='dispatch')
class HomeView(TemplateView):
    template_name = "home.html"


@method_decorator(login_required, name='dispatch')
class PortalHubView(View):

    @staticmethod
    def get(request):
        portals = Portals.objects.filter(guest=request.user)
        return render(request, 'portal_hub.html', {'portals': portals})

    @staticmethod
    def post(request):
        website = request.POST.get("website")
        portal_name = request.POST.get("portal_name")
        domain = get_domain_from_url(website)
        check_another_portal = Portals.objects.filter(guest=request.user, domain=domain)
        if not check_another_portal:
            portal = Portals(
                guest=request.user,
                portal_name=portal_name,
                domain=domain,
            )
            portal.save()

        return redirect(reverse('portal', args=[website]))


@method_decorator(login_required, name='dispatch')
class PortalView(View):

    @staticmethod
    def get(request, website, path=None):
        data = requests.get(website)
        domain = get_domain_from_url(website)
        portal = get_object_or_404(Portals, domain=domain)
        soup = BeautifulSoup(data.content, 'lxml')
        data_size_mb = Decimal(len(data.content)) / Decimal(1024 * 1024)
        portal.data_volume += data_size_mb
        portal.page_views += 1
        portal.save()

        modify_links(soup, domain)
        html_content = soup.prettify()
        return render(request, 'portal.html', {'html_content': html_content})


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
            return redirect(reverse("home"))
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
        return redirect(reverse("home"))


@method_decorator(login_required, name='dispatch')
class LogoutView(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        logout(request)
        return redirect(reverse_lazy("login"))
