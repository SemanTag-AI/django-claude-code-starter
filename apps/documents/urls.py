"""URLs of the documents app."""

from django.urls import path

from . import views

app_name = "documents"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path("documents/", views.DocumentListView.as_view(), name="list"),
    path("documents/new/", views.DocumentCreateView.as_view(), name="new"),
    path("documents/<int:pk>/", views.DocumentDetailView.as_view(), name="detail"),
    path("documents/<int:pk>/review/", views.ReviewView.as_view(), name="review"),
]
