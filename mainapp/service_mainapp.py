from django.db.models import QuerySet

from mainapp.models import Hab, HabCategory


def last_hub(n: int) -> QuerySet:
    """Функция выбирает n последних статей"""
    query_set = Hab.objects.all().order_by("creat_time")
    count = query_set.count()
    if count < n:
        return query_set
    query_set = query_set[count-n:count:-n]
    return query_set


def all_HabCategory() -> QuerySet:
    """Функция выбирает все категории статей"""
    query_set = HabCategory.objects.all()
    return query_set
