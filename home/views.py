from django.shortcuts import render


def home(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


def academy(request):
    return render(request, "academy.html")


def live_event(request):
    return render(request, "live-event.html")


def plans(request):
    return render(request, "plans.html")