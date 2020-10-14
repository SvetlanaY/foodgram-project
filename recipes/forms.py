from django.db import models

from .models import Recipe, Tag
from django import forms
from django.forms.widgets import CheckboxSelectMultiple


class RecipeCreateForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ("name", "image", "tag", "time", "description",)
        widgets = {'tag': CheckboxSelectMultiple(), }
    # def clean_title(self):
    #     name=self.cleaned_data['name']
    #     if name.lower() in ('create'):
    #         raise ValidationError(f'Недопустимое имя "{name}"')
    #     return name
    # def __init__(self, data=None, *args, **kwargs):
    #     if data is not None:
    #         data = data.copy()
    #         for k in ('breakfast', 'lunch', 'dinner'):
    #             if k in data:
    #                 data.update({'tag': k})
    #     super().__init__(data=data, *args, **kwargs)
