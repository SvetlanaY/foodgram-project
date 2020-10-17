import csv
import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Sum
from django.http import HttpResponse, JsonResponse, request
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RecipeCreateForm
from .models import (Favorite, Follow, Ingredient, IngredientRecipe, Recipe, ShopList, Tag, User)
from .utils import get_ingredients

def index(request):
    tags_for_page_filter = ''
    tags = Tag.objects.all()
    if "filters" in request.GET:
        filters = request.GET.getlist("filters")
        recipes = Recipe.objects.filter(
            tag__slug__in=filters).order_by("-pub_date").distinct()
        tags_for_page = ''
        for filter in filters:
            tags_for_page += "filters="+filter+"&"
        tags_for_page_filter = tags_for_page[:-1]
    else:
        recipes = Recipe.objects.all().order_by("-pub_date")

    paginator = Paginator(recipes, 6)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    context = {
        "page": page,
        "paginator": paginator,
        "tags": tags,
        "filters": tags_for_page_filter
    }

    if request.user.is_authenticated:
        favorites = Favorite.objects.get_or_create(user=request.user)[0].recipes.all()
        shops = ShopList.objects.get_or_create(user=request.user)[0].recipes.all()
        context["favorites"] = favorites
        context["shops"] = shops

        return render(request, "indexAuth.html", context)
    return render(request, "indexNotAuth.html", context)


@login_required
def ingredient_add(request):
    query = request.GET["query"]
    ingredients = Ingredient.objects.filter(name__istartswith=query).extra(
        select={"title": "name"}).values("title", "dimension")
    return JsonResponse(list(ingredients), safe=False)


@login_required
def new_recipe(request):
    if request.method == "POST":
        form = RecipeCreateForm(request.POST, files=request.FILES or None)
        ingredients = get_ingredients(request)
        if not ingredients:
            form.add_error(None, "Добавьте хотя бы один ингредиент")
        elif form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            objs = [IngredientRecipe(amount=amount, ingredient=Ingredient.objects.get(
                name=name), recipe=recipe) for name, amount in ingredients.items()]
            IngredientRecipe.objects.bulk_create(objs)
            form.save_m2m()
            return redirect("recipe_id", recipe_id=recipe.id)
    else:
        form = RecipeCreateForm(files=request.FILES or None)
    shops = ShopList.objects.get_or_create(user=request.user)[0].recipes.all()

    return render(request, "formRecipe.html", {"form": form, "shops": shops})


@login_required
def recipe_edit(request, recipe_id):
    edit = True
    recipe = get_object_or_404(
        Recipe.objects.prefetch_related("tag"), id=recipe_id)
    if request.user != recipe.author:
        return redirect("recipe_id", recipe_id=recipe_id)
    if request.method == "POST":
        form = RecipeCreateForm(
            request.POST, files=request.FILES or None, instance=recipe)
        ingredients = get_ingredients(request)
        if not ingredients:
            form.add_error(None, "Добавьте хотя бы один ингредиент")
        if form.is_valid():
            form.save()
            recipe.ingredientrecipe_set.all().delete()
            objs = [IngredientRecipe(amount=amount, ingredient=Ingredient.objects.get(
                name=name), recipe=recipe) for name, amount in ingredients.items()]
            IngredientRecipe.objects.bulk_create(objs)
            return redirect("recipe_id", recipe_id=recipe_id)
    else:
        form = RecipeCreateForm(instance=recipe)

    return render(request, "formRecipe.html", {"form": form,  "edit": edit})


@login_required
def recipe_delete(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user == recipe.author:
        recipe.delete()
        return redirect("profile", username=recipe.author.username)
    return redirect("recipe_id", recipe_id=recipe_id)


def recipe_view_id(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    if request.user.is_authenticated:
        favorites = Favorite.objects.get_or_create(user=request.user)[0].recipes.all()
        subscriptions = Follow.objects.get_or_create(user=request.user)[0].author.all()
        shops = ShopList.objects.get_or_create(user=request.user)[0].recipes.all()

        return render(request, "singlePage.html", {"recipe": recipe, "favorites": favorites, "subscriptions": subscriptions, "shops": shops})
    return render(request, "singlePageNotAuth.html", {"recipe": recipe})


@login_required
def follow_index(request):
    authors = Follow.objects.get_or_create(user=request.user)[0].author.prefetch_related("recipes")
    recipes = Recipe.objects.filter(author__in=authors).all().order_by("-pub_date")
    shops = ShopList.objects.get_or_create(user=request.user)[0].recipes.all()
    count_recipes = {}
    for author in authors:
        count_recipes[author.username] = Recipe.objects.filter(author=author).count()-3
    recipes_for_print = []
    for author in authors:
        recipes_for_print.append(Recipe.objects.filter(author=author).order_by("-pub_date")[:3])
    paginator = Paginator(authors, 6)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    context = {
        "page": page,
        "paginator": paginator,
        "recipes": recipes,
        "authors": authors,
        "count_recipes": count_recipes,
        "shops": shops,
        "recipes_for_print": recipes_for_print
    }

    return render(request, "myFollow.html", context)


@login_required
def profile_follow(request):
    id = json.loads(request.body).get("id")
    author = get_object_or_404(User, id=id)
    if author == request.user:
        return JsonResponse({"success": False})
    follower = Follow.objects.get_or_create(user=request.user)
    follower[0].author.add(author)
    return JsonResponse({"success": True})


@login_required
def profile_unfollow(request, id):
    profile = get_object_or_404(User, id=id)
    follows = get_object_or_404(Follow, user=request.user)
    follows.author.remove(profile)
    return JsonResponse({"success": True})


@login_required
def favorite_index(request):
    tags_for_page_filter = ''
    tags = Tag.objects.all()
    if "filters" in request.GET:
        filters = request.GET.getlist("filters")
        recipes = Favorite.objects.get(user=request.user).recipes.filter(
            tag__slug__in=filters).order_by("-pub_date").distinct()
        tags_for_page = ""
        for filter in filters:
            tags_for_page += "filters="+filter+"&"
        tags_for_page_filter = tags_for_page[:-1]
    else:
        recipes = Favorite.objects.get(
            user=request.user).recipes.order_by("-pub_date")

    shops = ShopList.objects.get_or_create(user=request.user)[0].recipes.all()

    paginator = Paginator(recipes, 6)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    context = {
        "page": page,
        "paginator": paginator,
        'tags': tags,
        'filters': tags_for_page_filter,
        "shops": shops,
    }

    return render(request, "favorite.html", context)


@login_required
def favorites_add(request):
    id = json.loads(request.body).get("id")
    favorite_recipe = get_object_or_404(Recipe, id=id)
    user_favorites = Favorite.objects.get_or_create(user=request.user)
    user_favorites[0].recipes.add(favorite_recipe)
    return JsonResponse({"success": True})


@login_required
def favorites_delete(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    user_favorites = get_object_or_404(Favorite, user=request.user)
    user_favorites.recipes.remove(recipe)
    return JsonResponse({"success": True})


@login_required
def shops(request):
    shops = ShopList.objects.get(user=request.user).recipes.order_by("-pub_date")
    return render(request, "shopList.html", {"shops": shops})


def purchases_add(request):
    recipe_id = json.loads(request.body).get("id")
    recipe = get_object_or_404(Recipe, id=recipe_id)
    shops = ShopList.objects.get_or_create(user=request.user)
    shops[0].recipes.add(recipe)
    return JsonResponse({"success": True})


def purchases_delete(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    shops = get_object_or_404(ShopList, user=request.user)
    shops.recipes.remove(recipe)
    return JsonResponse({"success": True})


def download_shops(request):
    shops = get_object_or_404(ShopList, user=request.user)
    recipes = shops.recipes.all()
    ingredients = IngredientRecipe.objects.filter(recipe__in=recipes).select_related("ingredient").values(
        "ingredient__name", "ingredient__dimension").annotate(amounts=Sum("amount")).all()

    response = HttpResponse(content_type="text/txt")
    response["Content-Disposition"] = 'attachment; filename="shops.txt"'

    writer = csv.writer(response)

    for ingredient in ingredients:
        name = ingredient["ingredient__name"]
        dimension = ingredient["ingredient__dimension"]
        amounts = ingredient["amounts"]
        writer.writerow([f"{name} ({dimension}) - {amounts}"])

    return response


def page_not_found(request, exception):
    return render(request, "404.html", {"path": request.path}, status=404)


def server_error(request):
    return render(request, "500.html", status=500)
