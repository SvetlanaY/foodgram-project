from django.db import models
from django.forms import ModelForm
from .models import Recipe,Tag
from django import forms
from django.forms.widgets import CheckboxSelectMultiple


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ["author", "name", "image", "tag", "time"]

       

# class RecipeCreateOrUpdateForm(ModelForm):
#     tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), to_field_name='slug')
    
#     class Meta:
#         model = Recipe
#         fields = ("author",'name','image','time','tags', )

#     def __init__(self, data=None, *args, **kwargs):
#         if data is not None:
#             data = data.copy()
#             for k in ('breakfast', 'lunch', 'dinner'):
#                 if k in data:
#                     data.update({'tags': k})
#         super().__init__(data=data, *args, **kwargs)        

class RecipeCreateForm(forms.ModelForm):
    class Meta:
        model=Recipe
        fields=("author", "name", "image", "tag", "time","description",)
        widgets={'tag': CheckboxSelectMultiple(),}
    def clean_title(self):
        name=self.cleaned_data['name']
        if name.lower() in ('create'):
            raise ValidationError(f'Недопустимое имя "{name}"')
        return name