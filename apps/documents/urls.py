"""URLs of the documents app."""

from django.urls import path

from .views import NotWrittenYetView

app_name = "documents"

urlpatterns = [
    path("", NotWrittenYetView.as_view(), name="home"),
    path("dashboard/", NotWrittenYetView.as_view(), name="dashboard"),
    path("documents/", NotWrittenYetView.as_view(), name="list"),
    path("documents/new/", NotWrittenYetView.as_view(), name="new"),
    path("documents/<int:pk>/", NotWrittenYetView.as_view(), name="detail"),
    path("documents/<int:pk>/review/", NotWrittenYetView.as_view(), name="review"),
]
