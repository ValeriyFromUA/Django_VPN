from core.views import (HomeView, LoginView, LogoutView, PortalHubView,
                        PortalView, RegistrationView)
from django.urls import path

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegistrationView.as_view(), name="register"),
    path("home/", HomeView.as_view(), name="home"),
    path("", HomeView.as_view(), name="home_main"),
    path('portal_hub/', PortalHubView.as_view(), name='portal_hub'),
    path('portal/<path:website>/', PortalView.as_view(), name='portal'),
]
