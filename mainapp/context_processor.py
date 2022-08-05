from habapp.models import Category


def menu_category_context(request):

    categories = Category.objects.all().filter(is_active=True)

    return {
        'categories': categories
        }
