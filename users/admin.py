from django.contrib import admin

from recipes.models import Follow


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', )
    search_fields = ('user', )
    filter_horizontal = ('author', )


admin.site.register(Follow, FollowAdmin)