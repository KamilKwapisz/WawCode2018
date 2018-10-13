from django.core import serializers
from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth import views as auth_views
from django.http import HttpResponse, JsonResponse
from django.views.generic import View, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils import timezone
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.decorators.debug import sensitive_variables, sensitive_post_parameters
from django.utils.decorators import method_decorator
import json

from .models import Lokal, Comment
from .forms import UserForm
from .utils import *


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def profile(request):
    context = {}
    return render(request, 'chlanie/profile.html', context)


def searchtest(request):
    context = {}
    return render(request, 'chlanie/searchtest.html', context)


class RegisterView(View):
    form_class = UserForm
    template_name = "registration/registration.html"

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    @method_decorator(sensitive_variables())
    @method_decorator(sensitive_post_parameters())
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid() and form.cleaned_data['password'] == form.cleaned_data['password_confirm']:
            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.email = username
            user.set_password(password)
            user.save()

            # returns user object if credentials are OK
            user = authenticate(username=username, password=password)
            print(user)

            if user is not None:
                messages.success(self.request, "User {} has been created!".format(username))
            else:
                messages.error(self.request, "Invalid email or password")

        elif form.data['password'] != form.data['password_confirm']:
            form.add_error('password_confirm', 'Passwords do not match')

        return render(request, self.template_name, {'form': form})


class LokalDetailView(DetailView):
    model = Lokal
    template_name = "chlanie/lokal.html"

    def get_context_data(self, **kwargs):
        lokal = self.get_object()

        info = {
            "data": {
                "fastfood": lokal.jedzenie,
                "face": lokal.regionalne,
                "mic": lokal.karaoke,
                "smoking_rooms": lokal.palarnia,
                "weekend": lokal.ogrodek,
                "battery_charging_full": lokal.ladowanieTelefonu,
                "music_note": lokal.parkiet,
                "tv": lokal.mecze},
            "dictionary": {
                "fastfood": "Jedzenie",
                "face": "Regionalne",
                "mic": "Karaoke",
                "smoking_rooms": "Palarnia",
                "weekend": "Ogródek",
                "battery_charging_full": "Gniazdka",
                "music_note": "Parkiet",
                "tv": "Mecze"
            }
        }.items()

        comments = Comment.objects.filter(lokal=lokal.id)

        context = dict(lokal=lokal, info=info, comments=comments)

        return context


class LokalCreateView(CreateView):
    model = Lokal
    fields = [
        'nazwa',
        'adres',
        'cenaWodki',
        'cenaPiwa',
        'jedzenie',
        'regionalne',
        'godzinyOtwarcia',
        'karaoke',
        'palarnia',
        'ogrodek',
        'ladowanieTelefonu',
        'parkiet',
        'mecze',
    ]

    def form_valid(self, form):
        if form.is_valid():

            lokal = form.save(commit=False)
            # TODO validating adress string
            lokal.coordinates = address_to_coordinates(lokal.adres)
            return super(LokalCreateView, self).form_valid(form)
        else:
            messages.error("Invalid form")


def sample_query(request):
    lokale = Lokal.objects.all()
    user_location = "[52.217719, 20.991137]"
    radius = 1.0
    for lokal in lokale:
        dist = calculate_distance(lokal.coordinates, user_location)
        print(dist)
        if dist > radius:
            lokale = lokale.exclude(id=lokal.pk)

    context = dict(lokale=lokale)
    return render(request, 'chlanie/lokal_list.html', context)


def search_test(request):
    return render(request, 'chlanie/searchtest.html', {})


def get_lokals_list(request):
    data = request.GET.dict()
    for key, value in data.items():
        if value == 'true':
            data[key] = True
        elif value == 'false':
            data[key] = False
    print(data)
    data_without_prices = {k: v for k, v in data.items() if k not in ('cenaPiwa', 'cenaWodki')}
    lokale = Lokal.objects.filter(**data_without_prices)
    if 'cenaPiwa' in data.keys():
        lokale = lokale.filter(cenaPiwa__lte=data['cenaPiwa'])
    if 'cenaWodki' in data.keys():
        lokale = lokale.filter(cenaWodki__lte=data['cenaWodki'])

    print(lokale)
    json_data = serializers.serialize('json', list(lokale))
    return JsonResponse(json_data, safe=False)


def logout_view(request):
    logout(request)
    context = {}
    return render(request, 'chlanie/logged_out.html', context)


def login(request, *args, **kwargs):
    # if request.method == 'POST':
    # if not request.POST.get('remember_me', None):
    #     request.session.set_expiry(0)
    return auth_views.login(request, *args, **kwargs)
