from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

counter = 0
profiles = {}


def index(request: HttpRequest) -> HttpResponse:
    global counter
    counter += 1
    return render(request, "index.html",
                  context={"title": "Home", "counter": counter})


def profile(request: HttpRequest, profile_id: int) -> HttpResponse:
    if request.method == "POST":
        profiles[profile_id] = request.POST
        return redirect("profile", profile_id=profile_id)
    if profile_id not in profiles:
        profiles[profile_id] = {'name': "John Doe", 'age': 25}
    context = {"profile": profiles[profile_id]}
    return render(request, "profile.html", context=context)


