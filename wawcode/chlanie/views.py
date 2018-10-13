from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth import views as auth_views
from django.http import HttpResponse
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils import timezone
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.decorators.debug import sensitive_variables, sensitive_post_parameters
from django.utils.decorators import method_decorator

from .models import Lokal

from .forms import UserForm


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def profile(request):
    context = {}
    return render(request, 'chlanie/profile.html', context)


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


class LokalCreateView(CreateView):
    model = Lokal
    fields = [
        'nazwa',
        'cenaPiwa',
        'cenaWodki',
        'jedznie',
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

            return super(LokalCreateView, self).form_valid(form)
        else:
            pass



def logout_view(request):
    logout(request)
    context = {}
    return render(request, 'chlanie/logged_out.html', context)


def login(request, *args, **kwargs):
    # if request.method == 'POST':
        # if not request.POST.get('remember_me', None):
        #     request.session.set_expiry(0)
    return auth_views.login(request, *args, **kwargs)
