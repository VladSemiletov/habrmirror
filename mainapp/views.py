from django.shortcuts import render

from core.context_service import context_update
from habapp.models import Like
from mainapp.service_mainapp import last_hub


def main(request):
    title = "Main"

    content = {"title": title}

    return render(request, "mainapp/index.html", content)


def about(request):
    title = "About"

    content = {"title": title}

    return render(request, "mainapp/about.html", content)


def help(request):
    title = "help"

    content = {"title": title}

    return render(request, "mainapp/help.html", content)
