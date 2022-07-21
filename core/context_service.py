from typing import Any


def context_update(context: dict, key: str, value: Any) -> dict:
    """Добавляет/обновляет пару key : value в словаре context """
    context.update({key: value})
    return context
