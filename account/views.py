from django.shortcuts import render, redirect, reverse
from .forms import LoginForm, OtpLoginForm, CheckOtpForm, UserEditForm, AddressCreationForm
from django.views import View
from django.contrib.auth import authenticate, login, logout
from .models import User, Otp
import ghasedakpack
from django.utils.crypto import get_random_string
from random import randint
from uuid import uuid4
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

SMS = ghasedakpack.Ghasedak('2abca38de138f1b7181033bcbf73347077490ec8872a6cdf0d2d072a2c7e115b')


# def user_login(request):
#     return render(request, 'account/login.html', {})

class UserLogin(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'account/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                form.add_error('username', 'invalid user data')
        else:
            form.add_error('username', 'invalid data')

        return render(request, 'account/login.html', {'form': form})


class OtpLoginView(View):
    def get(self, request):
        form = OtpLoginForm()
        return render(request, 'account/OtpLogin.html', {'form': form})

    def post(self, request):
        form = OtpLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            randcode = randint(1000, 9999)
            # SMS.verification({'receptor': cd['username'], 'type': '1', 'template': 'randcode', 'param1': randcode})
            token = str(uuid4())
            Otp.objects.create(phone=cd['phone'], code=randcode, token=token)
            print(randcode)
            return redirect(reverse('account:check_otp') + f'?token={token}')
        else:
            form.add_error('phone', 'invalid data')

        return render(request, 'account/OtpLogin.html', {'form': form})


class CheckOtpView(View):
    def get(self, request):
        form = CheckOtpForm()
        return render(request, 'account/check_otp.html', {'form': form})

    def post(self, request):
        token = request.GET.get('token')
        form = CheckOtpForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if Otp.objects.filter(code=cd['code'], token=token).exists():
                otp = Otp.objects.get(token=token)
                user, is_create = User.objects.get_or_create(phone=otp.phone)
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                otp.delete()
                return redirect('/')
        else:
            form.add_error('username', 'invalid data')

        return render(request, 'account/check_otp.html', {'form': form})


class UserLogoutView(LoginRequiredMixin, View):

    def get(self, request):
        logout(request)
        messages.success(request, 'شما با موفقیت خارج شدید', 'success')
        return redirect('home:home')


class UserEditProfile(LoginRequiredMixin, View):
    def get(self, request):
        form = UserEditForm()
        return render(request, 'account/edit_profile.html', {'form': form})

    def post(self, request):
        user = request.user
        form = UserEditForm(instance=user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('home:home')

        return render(request, 'account/edit_profile.html', context={'form': form})


class AddAddressView(View):
    def post(self, request):
        form = AddressCreationForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            next_page = request.GET.get('next')
            if next_page:
                return redirect(next_page)
        return render(request, 'account/add_address.html', {'form': form})

    def get(self, request):
        form = AddressCreationForm(request.POST)
        return render(request, 'account/add_address.html', {'form': form})
