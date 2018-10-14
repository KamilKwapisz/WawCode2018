from django.core import serializers
from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.views.generic import View, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils import timezone
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.decorators.debug import sensitive_variables, sensitive_post_parameters
from django.utils.decorators import method_decorator
import json

from .models import Lokal, Comment, Rate, Like, Reservation
from .forms import UserForm, CommentForm
from .utils import *


def index(request):
    return render(request, "chlanie/index.html", {})


def profile(request):
    context = {}
    return render(request, 'chlanie/profile.html', context)


def searchtest(request):
    context = {}
    return render(request, 'chlanie/searchtest.html', context)


def lokal_detail_view(request, pk):
    lokal = Lokal.objects.get(pk=pk)
    user = request.user

    info = {
        "fastfood": lokal.jedzenie,
        "face": lokal.regionalne,
        "mic": lokal.karaoke,
        "smoking_rooms": lokal.palarnia,
        "weekend": lokal.ogrodek,
        "battery_charging_full": lokal.ladowanieTelefonu,
        "music_note": lokal.parkiet,
        "tv": lokal.mecze
    }.items()

    comments = Comment.objects.filter(lokal=lokal.id)

    was_rated = False
    if Rate.objects.filter(user=user, lokal=lokal):
        was_rated = True
    rates = Rate.objects.filter(lokal=lokal.id)
    rating = 0.0
    for rate in rates:
        rating += rate.rating
    try:
        rating /= rates.count()
        rating = float("%.2f" % rating)
    except ZeroDivisionError:
        rating = 0

    context = dict(lokal=lokal, info=info, comments=comments)
    context['rating'] = rating
    context['was_rated'] = was_rated

    if Like.objects.filter(user=user, lokal=lokal).count() == 1:
        context['liked'] = True

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.lokal = lokal
            comment.author = user
            comment.save()
        else:
            messages.error(request, 'Please correct errors above.')
    else:
        form = CommentForm(request.POST)
    context['form'] = form

    return render(request, "chlanie/lokal.html", context)


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
    # success_url = reverse_lazy('chlanie:detail'),}

    def form_valid(self, form):
        if form.is_valid():

            lokal = form.save(commit=False)
            # TODO validating adress string
            lokal.coordinates = address_to_coordinates(lokal.adres)
            return super(LokalCreateView, self).form_valid(form)
        else:
            messages.error("Invalid form")


def search_test(request):
    return render(request, 'chlanie/searchtest.html', {})


def get_lokals_list(request):
    data = request.GET.dict()
    print(data)
    # user_coordinates = data['coordinates']
    user_coordinates = "[52.220116, 21.012091]"
    try:
        radius = int(data['promien'])
    except Exception:
        radius = 20
    for key, value in data.items():
        if value == 'true':
            data[key] = True
        elif value == 'false':
            data[key] = False
    data_without_prices = {k: v for k, v in data.items() if k not in ('cenaPiwa', 'cenaWodki')}
    data_without_prices = {k: v for k, v in data_without_prices.items() if k not in ('coordinates', 'promien', 'adres')}
    print("DEBUG2, ", data_without_prices)
    lokale = Lokal.objects.filter(**data_without_prices)
    print("DEBUG ", lokale.count())
    if 'cenaPiwa' in data.keys():
        lokale = lokale.filter(cenaPiwa__lte=float(data['cenaPiwa']))
    if 'cenaWodki' in data.keys():
        lokale = lokale.filter(cenaWodki__lte=float(data['cenaWodki']))
    lokale = get_places_within_radius(lokale, user_coordinates, radius)

    print(lokale)
    json_data = serializers.serialize('json', list(lokale))
    print(json_data)
    return JsonResponse(json_data, safe=False)


def rate(request):
    data = request.GET.dict()
    rating = int(data['ocena'])
    lokal_id = data['idLokalu']
    username = data['username']
    user = User.objects.get(username=username)
    lokal = Lokal.objects.get(id=lokal_id)
    rate_query = Rate.objects.filter(user=user, lokal=lokal)
    if rate_query.count() == 1:
        old_rate = Rate.objects.get(user=user, lokal=lokal)
        if old_rate.rating == rating:
            old_rate.rating = 0
        else:
            old_rate.rating = rating
        old_rate.save()

    else:
        Rate.objects.create(user=user, lokal=lokal, rating=rating)
    return JsonResponse(True, safe=False)


def comment(request):
    data = request.GET.dict()
    text = data['komentarz']
    lokal_id = data['idLokalu']
    lokal = Lokal.objects.get(id=lokal_id)
    username = data['username']
    user = User.objects.get(username=username)
    Comment.objects.create(lokal=lokal, user=user, text=text)


def reservation(request):
    data = request.GET.dict()
    username = data['username']
    lokal_id = data['idLokalu']
    table_type = data['stolik']
    date = data['data_rezerwacji']
    user = User.objects.get(username=username)
    lokal = Lokal.objects.get(id=lokal_id)
    Reservation.objects.create(user=user, lokal=lokal,
                               table_type=table_type, date=date)
    msg = f"Rezerwacja {table_type} osobowego stolika na {date} została pomyślnie zapisana"
    print(msg)
    return JsonResponse({'msg': msg}, safe=False)



def logout_view(request):
    logout(request)
    context = {}
    return render(request, 'chlanie/logged_out.html', context)


def login(request, *args, **kwargs):
    # if request.method == 'POST':
    # if not request.POST.get('remember_me', None):
    #     request.session.set_expiry(0)
    return auth_views.login(request, *args, **kwargs)


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
