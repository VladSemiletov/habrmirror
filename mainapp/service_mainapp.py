from django.db.models import QuerySet

from habapp.models import Hab, Category


def last_hub(n: int) -> QuerySet:
    """Функция выбирает n последних статей"""
    query_set = Hab.objects.all().order_by("created") #Проверить получение QS
    count = query_set.count()
    if count > n:
        query_set = query_set[count-n:count]
    return query_set[::-1]


def all_HabCategory() -> QuerySet:
    """Функция выбирает все категории статей"""
    query_set = Category.objects.all()
    return query_set
