# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def home(request):
    kwargs = {}
    return render(request, 'home.html', kwargs)


@login_required
def panel(request):
    return render(request, 'panel.html')
