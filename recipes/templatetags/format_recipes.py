from django import template
from django.http import QueryDict

register = template.Library()

@register.filter
def format_recipes_count(word, count):  
       
    if count % 10 == 1 and count % 10 !=11:
        word += ''
    elif count % 10 == 2 or count % 10 == 3 or count % 10 == 4   and count % 10 !=12 and count % 10 !=13 and count % 10 !=14:
        word += 'a'
    else:
        word += 'ов'
    return word   