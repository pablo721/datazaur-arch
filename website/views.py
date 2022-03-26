import datetime
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import View, TemplateView
from django.urls import reverse
from .models import *
from .forms import *
from .utils import *
from markets.models import Currency, Watchlist, Portfolio
from data.constants import *


class HomeView(TemplateView):
    template_name = 'website/home.html'


def home(request):
    context = {}
    if request.user.is_authenticated:
        print('authed')
        context['user'] = request.user
        context['currency_form'] = SelectCurrency()
        profile = Profile.objects.get(user=request.user)


    if request.method == 'POST' and 'currency' in str(request.POST):
        print(request.POST)

        currency_form = SelectCurrency(request.POST)
        if currency_form.is_valid():
            data = currency_form.cleaned_data
            user = request.user
            user.currency = Currency.objects.get(symbol=data['currency'])
            user.save()
            print(user.currency.name)


        else:
            print(f'errors: {currency_form.errors}')

    return render(request, 'website/home.html', context)


class LoginView(View):
    template_name = 'website/login.html'
    templates = {'success': 'website/home.html', 'fail': 'website/login_failed.html'}
    form = AuthenticationForm

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        context = self.get_context_data()
        if user is not None:
            request.session.set_expiry(87400)
            login(request, user)
            return render(request, self.templates['success'], context)
        else:
            return render(request, self.templates['fail'], context)

    def get_context_data(self, **kwargs):
        return {'form': self.form}


def log_in(request):
    if request.method == 'POST' and 'password' in request.POST:
        print(request.POST)
        user = authenticate(username=request.POST['username'], password=request.POST['password'])

        print(user)
        if user is not None:
            request.session.set_expiry(86400)
            login(request, user)
            context = {'user': user}
            return render(request, 'website/home.html', context)
        else:
            context = {'form': AuthenticationForm}
            return render(request, 'website/login_failed.html', context)
    else:
        return render(request, 'website/login.html', {'form': AuthenticationForm})


class SignUpView(View):
    template_name = 'website/signup.html'
    templates = {'success': 'website/home.html', 'fail': 'website/signup_failed.html'}
    form = UserCreationForm

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user_form = self.form(request.POST)
        if user_form.is_valid():
            form_data = user_form.cleaned_data
            ip = get_client_ip(request)
            try:
                location = get_location(ip)
            except:
                location = ''
            user = User.objects.create_user(username=form_data['username'], password=form_data['password1'])
            Account.objects.create(user=user, signup_ip=ip, signup_location=location)
            login(request, user)
            return render(request, self.templates['success'])
        else:
            context = {'errors': dict(user_form.errors)}
            return render(request, self.templates['fail'], context)

    def get_context_data(self, **kwargs):
        return {'form': self.form}




def signup(request):
    context = {'form': UserCreationForm, 'currencies': Currency.objects.all()}

    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            form_data = user_form.cleaned_data
            user = MyUser.objects.create_user(username=form_data['username'], password=form_data['password1'])
            request.session.set_expiry(86400)
            login(request, user)
            Watchlist.objects.create(user=profile)
            Portfolio.objects.create(user=profile)
            return render(request, 'website/home.html', context)

        else:
            print(user_form.errors)
            context['errors'] = dict(user_form.errors)
            print(context['errors'])
            return render(request, 'website/signup_failed.html', context)

    else:
        return render(request, 'website/signup.html', context)


class LogoutView(View):
    template_name = 'website/logout.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        return render(request, self.template_name)


def log_out(request):
    logout(request)
    return render(request, 'website/logout.html')


