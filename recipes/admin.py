from django.contrib import admin

from .models import Follow, Ingredient, IngredientRecipe, Recipe, Tag


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "dimension", "id")
    list_filter = ("name",)
    search_fields = ("name", )
    empty_value_display = "-пусто-"  # noqa


class RecipeAdmin(admin.ModelAdmin):
    def favorites_count(self, obj):
        return obj.favorites.count()

    favorites_count.short_description = "Число добавлений в Избранное"
    search_fields = ("name", )
    list_filter = ("tag", "name", "author", )
    readonly_fields = ("favorites_count", )
    list_display = ("name", "author", "pub_date")
    date_hierarchy = "pub_date"
    empty_value_display = "-пусто-"  # noqa


class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    empty_value_display = "-пусто-"   # noqa


class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = ("ingredient", "recipe", "amount")
    list_filter = ("recipe", "ingredient")
    empty_value_display = "-пусто-"  # noqa


class FollowAdmin(admin.ModelAdmin):
    list_display = ("user", )
    search_fields = ("user", )
    filter_horizontal = ("author", )


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(IngredientRecipe, IngredientRecipeAdmin)
admin.site.register(Follow, FollowAdmin)
