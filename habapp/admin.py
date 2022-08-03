from django.contrib import admin
from articleapp.models import Category, Article, Like


class HabAdmin(admin.ModelAdmin):
    """
    класс - Статьи в админке
    """
    list_display = (
        'author',
        'title',
        'content',
        'created',
        'updated',
        'approve'
    )
    list_filter = (
        'approve',
        'created'
    )
    actions = ['approve_hab']
    list_per_page = 5

    def approve_hab(self, request, queryset):
        """
        :param request:
        :param queryset:
        :return:
        """
        queryset.update(approve=True)


admin.site.register(Category)
admin.site.register(Article, HabAdmin)
admin.site.register(Like)
