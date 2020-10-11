import json,csv

import codecs
from django.db.models import F, Sum
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models.aggregates import Count,Sum
from django.http import HttpResponse, HttpResponseRedirect, request
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RecipeForm,RecipeCreateForm
from .models import Recipe,Follow,User,Ingredient_Recipe,Favorite,Tag,Ingredient,ShopList

def get_ingredients(request):
    ingredients = {}
    for key in request.POST:
        if key.startswith('nameIngredient'):
            value_ingredient = key[15:].encode('unicode-escape').decode('unicode-escape')

            ingredients[request.POST[key]] = request.POST['valueIngredient_' + value_ingredient]

    return ingredients



def index(request):       
    tags_for_page_filter=''    
    tags=Tag.objects.all()
    if 'filters' in request.GET:
        filters = request.GET.getlist("filters")
        recipes_list=Recipe.objects.filter(tag__slug__in=filters).order_by("-pub_date").distinct()        
        tags_for_page=''
        for filter in filters:
            tags_for_page+="filters="+filter+"&"
        tags_for_page_filter=tags_for_page[:-1]      
    else:
        recipes_list = (Recipe.objects.all().order_by("-pub_date")) 
        
    paginator = Paginator(recipes_list, 3) 
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)   
             

    if request.user.is_authenticated:
        favorites = Favorite.objects.get_or_create(user=request.user)[0].recipes.all()  
        shop_list = ShopList.objects.get_or_create(user=request.user)[0].recipes.all() 
        return render(request, "indexAuth.html", {"page": page, "paginator": paginator, "tags": tags, "filters":tags_for_page_filter,"favorites":favorites,"shop_list":shop_list})
    return render(request, "indexNotAuth.html", {"page": page, "paginator": paginator,"tags": tags,"filters":tags_for_page_filter})


def ingredient_add(request):
    query=request.GET['query']
    ingredients=Ingredient.objects.filter(name__istartswith=query).values('name', 'dimension').order_by()
    # ingredients=[]
    # for i in ingredients_1:
    #     ingredients.append({"name":i['name'].encode().decode(),"dimension":i['dimension'].encode('unicode-escape').decode('unicode-escape')})
       
   
    
    
    return JsonResponse(list(ingredients), safe=False)

      

  
@login_required
def new_recipe(request):
    new_recipe = True

    if request.method == 'POST':
        form = RecipeCreateForm(request.POST , files=request.FILES or None)
        ingredients = get_ingredients(request)
        if not bool(ingredients):
            form.add_error(None, "Добавьте хотя бы один ингредиент")

        elif form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()

            objs = [Ingredient_Recipe(amount=amount, ingredient=Ingredient.objects.get(name=name),recipe=recipe) for name, amount in ingredients.items()]

            Ingredient_Recipe.objects.bulk_create(objs)
            form.save_m2m()
            return redirect('recipe_id', recipe_id=recipe.id)

    else:
        form = RecipeCreateForm(files=request.FILES or None)
    shop_list = ShopList.objects.get_or_create(user=request.user)[0].recipes.all()     

    return render(request, 'formRecipe.html', {'form': form,'new_recipe': new_recipe,"shop_list":shop_list})
    #    context = {
    #     "title": "Создание рецепта",
    #     "button": "Создать рецепт",
    #     "form": form,
         
    # }
    # if request.method == "POST":
    #     if form.is_valid():
    #         recipe = form.save(commit=False)
    #         recipe.author = request.user
    #         recipe.save()
    #         return redirect("index")
    # return render(request, "formRecipe.html", context)

# class RecipeCreateView(LoginRequiredMixin, CreateView):
#     form_class = RecipeCreateOrUpdateForm    


def profile(request, username):
    profile = get_object_or_404(User, username=username)
    recipes = Recipe.objects.filter(author=profile).order_by("-pub_date").all()
    

    tags_for_page_filter=''    
    tags=Tag.objects.all()
    if 'filters' in request.GET:
        filters = request.GET.getlist("filters")
        recipes_list=Recipe.objects.filter(tag__slug__in=filters,author=profile).order_by("-pub_date").distinct()        
        tags_for_page=''
        for filter in filters:
            tags_for_page+="filters="+filter+"&"
        tags_for_page_filter=tags_for_page[:-1]      
    else:
        recipes_list = recipes
     
    paginator = Paginator(recipes_list, 3)
    page_number = request.GET.get("page")    
    page = paginator.get_page(page_number)

   

    context = {
      
        "page": page,
        "paginator": paginator,
      
        "author": profile,
      
        "tags": tags,
        "filters":tags_for_page_filter
    }

    if request.user.is_authenticated:
        favorites = Favorite.objects.get_or_create(user=request.user)[0].recipes.all() 
        subscriptions = Follow.objects.get_or_create(user=request.user)[0].author.all() 
        shop_list = ShopList.objects.get_or_create(user=request.user)[0].recipes.all()
        context["favorites"]=favorites
        context["subscriptions"] = subscriptions
        context["shop_list"] = shop_list


    return render(request, "authorRecipe.html", context)


def recipe_view(request, username, recipe_id):
    profile = get_object_or_404(User, username=username)
    recipes = Recipe.objects.filter(author=profile).all()
    recipe = Recipe.objects.get(id=recipe_id)
    recipe_count = Recipe.objects.filter(author=profile).count()
    shop_list = ShopList.objects.get_or_create(user=request.user)[0].recipes.all()

    

    context = {
        "recipes": recipes,
        "recipe": recipe,
        "recipe_count": recipe_count,
        "author": profile,
        "shop_list":shop_list
       
    }

    if request.user.is_authenticated:
    
        return render(request, "singlePage.html", context)
    return render(request, "singlePageNotAuth.html", context)

def recipe_view_id (request, recipe_id):
   
    recipe = Recipe.objects.get(id=recipe_id)
    

    

    if request.user.is_authenticated:
        favorites = Favorite.objects.get_or_create(user=request.user)[0].recipes.all()   
        subscriptions = Follow.objects.get_or_create(user=request.user)[0].author.all() 
        shop_list = ShopList.objects.get_or_create(user=request.user)[0].recipes.all()
    
        return render(request, "singlePage.html", {"recipe": recipe,"favorites":favorites,"subscriptions":subscriptions,"shop_list":shop_list})
    return render(request, "singlePageNotAuth.html", {"recipe": recipe})  


# def post_edit(request, username, post_id):
#     post = get_object_or_404(Post, id=post_id)
#     user = get_object_or_404(User, username=username)

#     if request.user != user:
#         return redirect("post", username=user.username, post_id=post_id)

#     form = PostForm(request.POST or None,
#                     files=request.FILES or None, instance=post)
#     context = {
#         "title": "Редактировать запись",
#         "button": "Сохранить",
#         "post": post,
#         "form": form,
#     }
#     if request.method == "POST":
#         if form.is_valid():
#             post.save()
#             return redirect("post", username=user.username, post_id=post_id)
#     return render(request, "new_post.html", context)


# def post_remove(request, username, post_id):
#     post = get_object_or_404(Post, id=post_id)
#     if request.user != post.author:
#         return redirect("post", username=post.author, post_id=post.id)
#     post = get_object_or_404(Post, id=post_id)
#     post.delete()
#     return redirect("index")


def page_not_found(request, exception):
    return render(request, "404.html", {"path": request.path}, status=404)


def server_error(request):
    return render(request, "500.html", status=500)


# @login_required
# def add_comment(request, username, post_id):
#     post = get_object_or_404(Post, id=post_id)
#     user = get_object_or_404(User, username=username)
#     if request.method == "POST":
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.post = post
#             comment.author = request.user
#             comment.save()
#             return redirect("post", username=user.username, post_id=post_id)
#     form = CommentForm()
#     return redirect("post", username=user.username, post_id=post_id)


@login_required
def follow_index(request):
    authors = Follow.objects.get_or_create(user=request.user)[0].author.prefetch_related('recipes')
    recipes = Recipe.objects.filter(author__in=authors).all()
    shop_list = ShopList.objects.get_or_create(user=request.user)[0].recipes.all()
    count_recipes={}
    for author in authors:
        count_recipes[author.username]=Recipe.objects.filter(author=author).count()-3

    paginator = Paginator(recipes, 3)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    return render(request, "myFollow.html", {"page": page, "paginator": paginator, "recipes": recipes, "authors": authors,"count_recipes":count_recipes,"shop_list":shop_list})


# authors_list = FollowAuthor.objects.get_or_create(
#         user=request.user
#     )[0].authors.prefetch_related(
#         'recipes'
#     ).order_by('username')

#     paginator = Paginator(authors_list, 6)
#     page_number = request.GET.get('page')
#     page = paginator.get_page(page_number)
#     subscriptions = True

#     return render(
#         request, 'myFollow.html',
#         {'page': page, 'paginator': paginator, 'subscriptions': subscriptions})



@login_required
def profile_follow(request):    
    id = json.loads(request.body).get('id')
    author = get_object_or_404(User, id=id)
    if author == request.user:
            return JsonResponse({'success': False})
    follower = Follow.objects.get_or_create(user=request.user)
    follower[0].author.add(author)         
    return JsonResponse({'success': True})

  

@login_required
def profile_unfollow(request, id):
    profile = get_object_or_404(User, id=id)
    follows = get_object_or_404(Follow, user=request.user)
    follows.author.remove(profile)
    return JsonResponse({'success': True})



 


# @login_required
# def favorite_index(request):
#     if 'filters' in request.GET:
#         filters = request.GET.getlist('filters')

#         recipe_list = Favorite.objects.get(user=request.user).recipes.filter(tag__slug__in=filters).distinct().prefetch_related('tag').select_related('author').order_by('-pub_date').all()

#     else:
#         recipe_list = Favorite.objects.get(             user=request.user
#         ).recipes.prefetch_related(
#             'tag'
#         ).select_related(
#             'author'
#         ).all()

#     paginator = Paginator(recipe_list, 3)
#     page_number = request.GET.get('page')
#     page = paginator.get_page(page_number)
#    # favorite_page = True
#     tags = Tag.objects.all()

    # return render(
    #     request, 'favorite.html',
    #     {'page': page, 'paginator': paginator, 'tags': tags})


@login_required
def favorite_index(request):
    tags_for_page_filter=''    
    tags=Tag.objects.all()
    
    if 'filters' in request.GET:
        filters = request.GET.getlist('filters')

        recipes_list=Favorite.objects.get(user=request.user).recipes.filter(tag__slug__in=filters).order_by("-pub_date").distinct()        
        tags_for_page=''
        for filter in filters:
            tags_for_page+="filters="+filter+"&"
        tags_for_page_filter=tags_for_page[:-1]              

    else:
        recipes_list = Favorite.objects.get(user=request.user).recipes.order_by("-pub_date") 
       
    shop_list = ShopList.objects.get_or_create(user=request.user)[0].recipes.all()

    paginator = Paginator(recipes_list, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
   # favorite_page = True
   

    return render(
        request, 'favorite.html',
        {'page': page, 'paginator': paginator, 'tags': tags,'filters':tags_for_page_filter,"shop_list":shop_list})




@login_required
def favorites_add(request):
    id = json.loads(request.body).get('id')
    

 
    favorite_recipe = get_object_or_404(Recipe, id=id)
    user_favorites = Favorite.objects.get_or_create(user=request.user)

    user_favorites[0].recipes.add(favorite_recipe)
    # already_favorites = Favorite.objects.filter(recipes=favorite_recipe, user=request.user).exists()
    # if not already_favorites and request.user != profile:
    #     Favorite.objects.create(user=request.user, recipes=favorite_recipe)
         
    return JsonResponse({'success': True})

@login_required
def favorites_delete(request, id):

    recipe = get_object_or_404(Recipe, id=id)
    user_favorites = get_object_or_404(Favorite, user=request.user)
    user_favorites.recipes.remove(recipe)
    return JsonResponse({'success': True})





@login_required
def recipe_edit(request, recipe_id):
    new_recipe = True
    edit = True

    recipe = get_object_or_404(Recipe.objects.prefetch_related('tag'), id=recipe_id)

    if request.user != recipe.author:
        return redirect('recipe_id', recipe_id=recipe_id)

    if request.method == 'POST':
        form = RecipeCreateForm(request.POST, files=request.FILES or None, instance=recipe)
        ingredients = get_ingredients(request)

        if bool(ingredients) is False:
            form.add_error(None, "Добавьте хотя бы один ингредиент")

        if form.is_valid():
            form.save()
            recipe.ingredientamount_set.all().delete()

            objs = [Ingredient_Recipe(
                amount=amount, ingredient=Ingredient.objects.get(name=name),
                recipe=recipe) for name, amount in ingredients.items()]

            Ingredient_Recipe.objects.bulk_create(objs)
            return redirect('recipe_id', recipe_id=recipe_id)
    else:
        form = RecipeCreateForm(instance=recipe)

    return render(
        request, 'formRecipe.html',
        {'form': form, 'new_recipe': new_recipe, 'edit': edit})


@login_required
def recipe_delete(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user == recipe.author:
        recipe.delete()
        return redirect('profile', username=recipe.author.username)
    return redirect('recipe_id', recipe_id=recipe_id)
  
@login_required
def shop_list(request):   
    shop_list = ShopList.objects.get(user=request.user).recipes.order_by("-pub_date") 
    return render(request, 'shopList.html',{"shop_list":shop_list})

def purchases_add(request):
    recipe_id = json.loads(request.body).get('id')
    recipe = get_object_or_404(Recipe, id=recipe_id)

    shop_list = ShopList.objects.get_or_create(user=request.user)

    shop_list[0].recipes.add(recipe)
    return JsonResponse({'success': True})

def purchases_delete(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    shop_list = get_object_or_404(ShopList, user=request.user)
    shop_list.recipes.remove(recipe)
    return JsonResponse({'success': True})  


def download_shop_list(request):
    shop_list = get_object_or_404(ShopList, user=request.user)
    recipes = shop_list.recipes.all()

    ingredient_list = recipes.annotate(name1=F('ingredient_recipe__ingredient__name'),
        dimension=F('ingredient_recipe__ingredient__dimension')
    ).values(
        'name1', 'dimension'
    ).annotate(
        total=Sum('ingredient_recipe__amount')
    ).order_by('name1')

    response = HttpResponse(content_type='text/txt')
    response['Content-Disposition'] = 'attachment; filename="shop-list.txt"'

    writer = csv.writer(response)

    for ingredient in ingredient_list:
        name1 = ingredient['name1']
        dimension = ingredient['dimension']
        total = ingredient['total']
        writer.writerow([f'{name1} ({dimension}) - {total}'])

    return response