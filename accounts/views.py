# -*- coding: utf-8 -*-
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect

from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import update_session_auth_hash

from . import forms


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


@login_required
def settings(request):
    kwargs = {}

    kwargs['password_change_form'] = forms.UserPasswordChangeForm(prefix='password_change_form')
    kwargs['basic_data_change_form'] = forms.UserBasicDataChangeForm(prefix='basic_data_change_form',
                                                                     instance=request.user)

    return render(request, 'settings.html', kwargs)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = forms.UserPasswordChangeForm(data=request.POST, prefix='password_change_form')
        if form.is_valid():
            cleaned = form.cleaned_data

            old_password = cleaned['old_password']
            password1 = cleaned['new_password1']
            password2 = cleaned['new_password2']

            if password1 == password2 and check_password(password=old_password,
                                                         encoded=request.user.password,
                                                         setter=make_password(password=old_password,
                                                                              salt=None,
                                                                              hasher='default')):
                user = request.user
                user.password = make_password(password=password1,
                                              salt=None,
                                              hasher='default')
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Hasło zostało zmienione.")
            else:
                messages.error(request, "Obecne hasło jest nieprawidłowe i/lub nowe hasła się nie zgadzają.")
        else:
            messages.error(request, "Formularz został wypełniony nieprawidłowo, spróbuj ponownie.")
    return HttpResponseRedirect(reverse('settings'))


@login_required
def change_basic_data(request):
    if request.method == 'POST':
        form = forms.UserBasicDataChangeForm(data=request.POST,
                                             prefix='basic_data_change_form',
                                             instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Dane zostały zmienione.")
        else:
            messages.error(request, "Formularz został wypełniony nieprawidłowo, spróbuj ponownie.")
    return HttpResponseRedirect(reverse('settings'))
