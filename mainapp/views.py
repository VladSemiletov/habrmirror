from django.shortcuts import render

from core.context_service import context_update
from habapp.models import Like
from mainapp.service_mainapp import last_hub


def main(request):
    content = {}
    context_update(content, "title", "Main")
    context_update(content, "hab", last_hub(10))
    return render(request, "mainapp/index.html", content)


def about(request):
    title = "About"

    content = {"title": title}

    return render(request, "mainapp/about.html", content)


def help(request):
    title = "help"

    content = {"title": title}

    return render(request, "mainapp/help.html", content)
