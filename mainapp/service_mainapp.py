from django.db.models import QuerySet

from mainapp.models import Hab


def last_hub() -> QuerySet:
    """Функция выбирает последние 5 созданных статей"""
    query_set = Hab.objects.all().order_by("creat_time")[:5]
    return query_set
