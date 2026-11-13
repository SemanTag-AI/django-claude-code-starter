"""Views of the documents app. They ask the rules; they decide nothing themselves."""

from collections.abc import Iterable
from datetime import datetime
from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, RedirectView, TemplateView

from .choices import Status
from .forms import DocumentForm
from .models import Document
from .reviews import record_review
from .rules import is_overdue, may_review
from .summary import dashboard_summary

#: How many documents each list on the dashboard shows.
DASHBOARD_LIST_LENGTH = 5


def with_overdue_mark(documents: Iterable[Document], now: datetime) -> list[Document]:
    """Give every document an ``overdue`` attribute a template can read."""
    marked = list(documents)
    for document in marked:
        document.overdue = is_overdue(document, now)
    return marked


class HomeView(LoginRequiredMixin, RedirectView):
    """The start page is the dashboard, for whoever is signed in."""

    pattern_name = "documents:dashboard"


class DashboardView(LoginRequiredMixin, TemplateView):
    """Where the documents stand, and what waits for the signed-in user."""

    template_name = "documents/dashboard.html"

    def get_context_data(self, **kwargs: object) -> dict[str, Any]:
        """Add the numbers and the two short lists."""
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        to_review = Document.objects.filter(status=Status.WAITING).exclude(submitted_by=self.request.user)
        context["summary"] = dashboard_summary(self.request.user, now)
        context["to_review"] = with_overdue_mark(to_review.order_by("submitted_at")[:DASHBOARD_LIST_LENGTH], now)
        context["recent"] = with_overdue_mark(Document.objects.all()[:DASHBOARD_LIST_LENGTH], now)
        return context


class DocumentListView(LoginRequiredMixin, ListView):
    """Every document in the register, newest first."""

    model = Document
    template_name = "documents/list.html"
    context_object_name = "documents"

    def get_context_data(self, **kwargs: object) -> dict[str, Any]:
        """Mark the overdue documents."""
        context = super().get_context_data(**kwargs)
        context["documents"] = with_overdue_mark(context["documents"], timezone.now())
        return context


class DocumentCreateView(LoginRequiredMixin, CreateView):
    """Submit a document for review."""

    form_class = DocumentForm
    template_name = "documents/new.html"

    def form_valid(self, form: DocumentForm) -> HttpResponse:
        """Record who submitted the document. The form does not ask."""
        form.instance.submitted_by = self.request.user
        messages.success(self.request, "The document was submitted and waits for a review.")
        return super().form_valid(form)

    def get_success_url(self) -> str:
        """Show the document that was just submitted."""
        return reverse("documents:detail", args=[self.object.pk])


class DocumentDetailView(LoginRequiredMixin, DetailView):
    """One document, and the review if the signed-in user may give it."""

    model = Document
    template_name = "documents/detail.html"
    context_object_name = "document"

    def get_context_data(self, **kwargs: object) -> dict[str, Any]:
        """Say whether to offer the review and whether the document is overdue."""
        context = super().get_context_data(**kwargs)
        document = context["document"]
        document.overdue = is_overdue(document, timezone.now())
        context["offer_review"] = document.status == Status.WAITING and may_review(document, self.request.user)
        return context


class ReviewView(LoginRequiredMixin, View):
    """Record an approval or a rejection."""

    http_method_names = ["post"]

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        """Record the decision, or say why not.

        Hiding the buttons from the submitter is a courtesy. The refusal here is the control.
        """
        document = get_object_or_404(Document, pk=pk)
        decision = request.POST.get("decision")
        if decision not in (Status.APPROVED, Status.REJECTED):
            return HttpResponseBadRequest("A review is an approval or a rejection.")
        if record_review(document, request.user, Status(decision), timezone.now()):
            messages.success(request, f"The document was {decision}.")
        else:
            messages.warning(request, "This document was already reviewed. Nothing changed.")
        return redirect("documents:detail", pk=document.pk)
