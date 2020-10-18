from django.urls import path

from . import views

urlpatterns = [
    path("new/", views.new_recipe, name="new_recipe"),
    path("recipe/edit/<int:recipe_id>/",
         views.recipe_edit, name="recipe_edit"),
    path("recipe/delete/<int:recipe_id>/",
         views.recipe_delete, name="recipe_delete"),
    path("recipe/<int:recipe_id>/", views.recipe_view_id, name="recipe_id"),
    path("myfavorites/", views.favorite_index, name="favorites"),
    path("myfollow/", views.follow_index, name="follow_index"),
    path("shop-list/", views.shops, name="shops"),
    path("shop-list/download/", views.download_shops, name="download_shops"),

    path("subscriptions/<int:id>/",
         views.profile_unfollow, name="profile_unfollow"),
    path("subscriptions/", views.profile_follow, name="profile_follow"),
    path("ingredients/", views.ingredient_add, name="ingredient_add"),
    path("favorites/",
         views.favorites_add, name="favorites_add"),
    path("favorites/<int:id>/",
         views.favorites_delete, name="favorites_delete"),
    path("purchases/", views.purchases_add, name="purchases_add"),
    path("purchases/<int:recipe_id>/",
         views.purchases_delete, name="purchases_delete"),

    path("", views.index, name="index"),
]
