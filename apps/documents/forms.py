"""Forms of the documents app."""

from django import forms

from .choices import Tag
from .models import Document


class DocumentForm(forms.ModelForm):
    """What somebody fills in to submit a document."""

    tags = forms.MultipleChoiceField(
        choices=[(tag.value, tag.value) for tag in Tag],
        required=False,
        widget=forms.CheckboxSelectMultiple,
        error_messages={"invalid_choice": '"%(value)s" is not a valid choice.'},
    )

    class Meta:
        """The submitter, the status and the dates are not for the submitter to fill in."""

        model = Document
        fields = ["title", "body", "tags"]
