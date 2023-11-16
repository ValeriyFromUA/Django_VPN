from django.urls import path

from core.views import (RegistrationView, HomeView, LoginView, LogoutView, GuestProfileView, ProxyView, ProxyMoreView)

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegistrationView.as_view(), name="register"),
    path("home/", HomeView.as_view(), name="home"),
    path("profile/<str:pk>/", GuestProfileView.as_view(), name="profile"),
    path('proxy/', ProxyView.as_view(), name='proxy'),
    path('proxy_more/<path:website>/', ProxyMoreView.as_view(), name='proxy_more'),
]
