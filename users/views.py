from django.shortcuts import render, redirect
# позволяет узнать ссылку на URL по его имени, параметр name функции path
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CreationForm
from django.core.mail import send_mail

import json,csv




from django.core.paginator import Paginator

from django.http import HttpResponse, HttpResponseRedirect, request
from django.shortcuts import get_object_or_404, redirect, render


from recipes.models import Recipe,Follow,User,Favorite,Tag,ShopList


class SignUp(CreateView):
    form_class = CreationForm
    success_url = "/auth/login/"
    template_name = "signup.html" 

    send_mail(
        'Тема письма',
        'Текст письма.',
        'from@example.com',  
        ['to@example.com'],  
        fail_silently=False,  
    )


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
     
    paginator = Paginator(recipes_list, 6)
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


