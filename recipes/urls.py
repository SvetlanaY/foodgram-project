from django.urls import path

from . import views

urlpatterns = [
    path("recipe/edit/<int:recipe_id>", views.recipe_edit, name="recipe_edit"),
    path("subscriptions/<int:id>", views.profile_unfollow, name="profile_unfollow"),
    
    path("recipe/<int:recipe_id>/", views.recipe_view_id, name="recipe_id"),
    path("subscriptions/", views.profile_follow, name="profile_follow"),
    

    path("ingredients/", views.ingredient_add, name="ingredient_add"),
    path("favorites/", views.favorites_add, name="favorites_add"),
    path("myfavorites/", views.favorite_index, name="favorites"),
    path("myfollow/", views.follow_index, name="follow_index"),
    path("shop-list/", views.shop_list, name="shop_list"),
    path("shop-list/download/", views.download_shop_list, name="download_shop_list"),
    
    path("recipe/delete/<int:recipe_id>", views.recipe_delete, name="recipe_delete"),
    path("purchases/", views.purchases_add, name='purchases_add'),
    path("purchases/<int:recipe_id>/", views.purchases_delete,name='purchases_delete'),
   
    path("new/", views.new_recipe, name="new_recipe"),
  
    path("<username>/", views.profile, name="profile"),
    
    

    path("<username>/<int:recipe_id>/", views.recipe_view, name="recipe"),
   
    # path("<username>/<int:post_id>/edit", views.post_edit, name="post_edit"),
    # path('<username>/<int:post_id>/remove/', views.post_remove, name='post_remove'), 
    # path("<username>/<int:post_id>/comment/", views.add_comment, name="add_comment"),
    path("", views.index, name="index"),
    
    path("favorites/<int:id>", views.favorites_delete, name="favorites_delete"),
]