from django import template


register = template.Library()


@register.filter
def format_recipes_count(word, count):
    if count % 10 == 1 and count % 10 != 11:
        word += ''
    elif count % 10 in [2, 3, 4] and count % 100 not in [12, 13, 14]:
        word += 'a'
    else:
        word += 'ов'
    return word
