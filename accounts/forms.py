# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User


class UserBasicDataChangeForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class UserPasswordChangeForm(forms.Form):
    old_password = forms.CharField(label='Obecne hasło', min_length=8, widget=forms.PasswordInput, required=True)
    new_password1 = forms.CharField(label='Nowe hasło', min_length=8, widget=forms.PasswordInput, required=True)
    new_password2 = forms.CharField(label='Potwórz hasło', min_length=8, widget=forms.PasswordInput, required=True)
