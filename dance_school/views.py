from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def home_view(request: HttpRequest) -> HttpResponse:
    return render(request, "home.html")


def about_view(request: HttpRequest) -> HttpResponse:
    return render(request, "about.html")
