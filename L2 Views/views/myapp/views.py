from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, reverse


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "index.html")


def redirect_to_index(request: HttpRequest) -> HttpResponse:
    return redirect(reverse("myapp:home"))


def profile(request: HttpRequest, profile_id: int) -> HttpResponse:
    if not (0 < profile_id <= 100):
        return HttpResponseNotFound("Profile does not exist")
    return render(request, "profile.html", {"profile": profile_id})
