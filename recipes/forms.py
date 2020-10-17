from django import forms
from django.forms.widgets import CheckboxSelectMultiple

from .models import Recipe


class RecipeCreateForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ("name", "image", "tag", "time", "description",)
        widgets = {"tag": CheckboxSelectMultiple(), }
