from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def profile(request):
    context = dict(a="a")
    return render(request, 'chlanie/profile.html', context)
