from django.db.models import QuerySet

from mainapp.models import Hab, HabCategory


def last_hub() -> QuerySet:
    """Функция выбирает последние 5 созданных статей"""
    query_set = Hab.objects.all().order_by("creat_time")[:5:-1]
    return query_set


def all_HabCategory() -> QuerySet:
    """Функция выбирает все категории статей"""
    query_set = HabCategory.objects.all()
    return query_set
