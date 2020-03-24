# -*- coding: utf-8 -*-
from django import forms

from . import models


class SurveyCreationForm(forms.ModelForm):
    class Meta:
        model = models.Survey
        fields = ['name', 'description']


class QuestionCreationForm(forms.ModelForm):
    class Meta:
        model = models.Question
        fields = ['q_type', 'name', 'description']