from django.contrib import admin
from django.db import models
from .models import Recipe,Ingredient,Tag, Ingredient_Recipe,Favorite




class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "dimension", "id")
    list_filter = ("name",)
    search_fields = ('name', )
    empty_value_display = "-пусто-" # noqa



class RecipeAdmin(admin.ModelAdmin):
    def favorites_count(self, obj):
        return obj.favorite_recipes.count()

    favorites_count.short_description = 'Число добавлений в Избранное'
  
    search_fields = ('name', )
    list_filter = ('tag', 'name', 'author', )
     

    readonly_fields = ('favorites_count', )        
    list_display = ("name", "author",'pub_date')
    
    date_hierarchy = 'pub_date'
    empty_value_display = "-пусто-" # noqa


class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    empty_value_display = "-пусто-"   # noqa  


class Ingredient_RecipeAdmin(admin.ModelAdmin):
    list_display = ("ingredient", "recipe","amount")
    list_filter = ("recipe","ingredient")
    empty_value_display = "-пусто-" # noqa    



admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient_Recipe,Ingredient_RecipeAdmin)




