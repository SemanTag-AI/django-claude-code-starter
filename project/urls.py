"""URL configuration."""

from django.contrib.auth import views as auth_views
from django.urls import include, path

from apps.documents.views import HealthView

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("healthz/", HealthView.as_view(), name="health"),
    path("", include("apps.documents.urls")),
]
