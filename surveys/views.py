from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages

from . import forms
from .models import Survey, Question, Answer


@login_required
def surveys(request):
    kwargs = {}
    kwargs['surveys'] = Survey.objects.filter(user=request.user)
    return render(request, 'surveys.html', kwargs)


@login_required
def create(request):

    if request.method == 'GET':
        kwargs = {}
        kwargs['survey_creation_form'] = forms.SurveyCreationForm(prefix='survey-creation-form')
        return render(request, 'create.html', kwargs)

    elif request.method == 'POST':
        form = forms.SurveyCreationForm(data=request.POST, prefix='survey-creation-form')
        if form.is_valid():
            new_survey = form.save(commit=False)
            new_survey.user = request.user
            new_survey.save()

            messages.success(request, "Ankieta została utworzona, możesz przystąpić do tworzenia pytań.")
            return HttpResponseRedirect(reverse('survey',
                                                kwargs={
                                                    'survey_id': new_survey.id
                                                }))

    messages.error(request, "Niepoprawne wyołanie trasy, spróbuj ponownie.")
    return HttpResponseRedirect(reverse('surveys'))


@login_required
def survey(request, survey_id):
    try:
        user_survey = Survey.objects.get(id=survey_id)

        if request.method == 'GET':
            kwargs = {}
            kwargs['survey'] = user_survey
            kwargs['questions'] = Question.objects.filter(survey=user_survey
                                                          )
            kwargs['survey_edit_form'] = forms.SurveyCreationForm(prefix='survey-creation-form',
                                                                  instance=user_survey)
            return render(request, 'survey.html', kwargs)

        elif request.method == 'POST':
            form = forms.SurveyCreationForm(data=request.POST,
                                            prefix='survey-creation-form',
                                            instance=user_survey)
            if form.is_valid():
                form.save()
                messages.success(request, "Dane ankiety zostały zmienione.")
                return HttpResponseRedirect(reverse('survey',
                                                    kwargs={
                                                        'survey_id': survey_id
                                                    }))
    except Survey.DoesNotExist:
        messages.error(request, "Wybrana ankieta nie istnieje.")
        return HttpResponseRedirect(reverse('surveys'))


@login_required
def delete(request, survey_id):
    try:
        user_survey = Survey.objects.get(id=survey_id)
        user_survey.delete()
        messages.success(request, "Wybrana ankieta została usunięta.")

    except Survey.DoesNotExist:
        messages.error(request, "Wybrana ankieta nie istnieje.")

    return HttpResponseRedirect(reverse('surveys'))


@login_required
def create_question(request, survey_id):
    try:
        user_survey = Survey.objects.get(id=survey_id)

        if request.method == 'GET':
            kwargs = {}
            kwargs['survey'] = user_survey
            kwargs['question_creation_form'] = forms.QuestionCreationForm(prefix='question-creation-form')
            return render(request, 'question_create.html', kwargs)

        elif request.method == 'POST':
            form = forms.QuestionCreationForm(data=request.POST, prefix='question-creation-form')
            if form.is_valid():
                new_question = form.save(commit=False)
                new_question.survey = user_survey
                new_question.save()

                messages.success(request, "Pytanie zostało utworzone")
                return HttpResponseRedirect(reverse('survey',
                                                    kwargs={
                                                        'survey_id': user_survey.id
                                                    }))

    except Survey.DoesNotExist:
        messages.error(request, "Wybrana ankieta nie istnieje.")
        return HttpResponseRedirect(reverse('surveys'))


@login_required
def delete_question(request, survey_id, question_id):
    try:
        survey_question = Question.objects.get(id=question_id)
        survey_question.delete()
        messages.success(request, "Wybrane pytanie zostało usunięte.")

    except Question.DoesNotExist:
        messages.error(request, "Wybrane pytanie nie istnieje.")

    return HttpResponseRedirect(reverse('survey',
                                        kwargs={
                                            'survey_id': survey_id
                                        }))


def share(request, survey_id, survey_name):
    try:
        kwargs = {}
        user_survey = Survey.objects.get(id=survey_id)
        survey_questions = Question.objects.filter(survey_id=survey_id)

        if request.method == 'GET':
            kwargs['survey'] = user_survey
            kwargs['questions'] = survey_questions
            return render(request, 'share.html', kwargs)

        elif request.method == 'POST':
            first_name = request.POST['first-name']
            answers = "<p>"
            print(request.POST)
            for question in survey_questions:
                answers += "Pytanie: %s <br /> Odpowiedź: <em>%s" % (question.name,
                                                                     request.POST.get(str(question.id), "Brak"))
                answers += "</em><br /><br />"
            answers += "</p>"

            new_answer = Answer()
            new_answer.user = user_survey.user
            new_answer.survey = user_survey
            new_answer.first_name = first_name
            new_answer.answers = answers
            new_answer.save()

            messages.success(request, "Dziękujemy, Twoje odpowiedzi zostały przesłane.")
            return HttpResponseRedirect(reverse('share-survey',
                                                kwargs={
                                                    'survey_id': user_survey.id,
                                                    'survey_name': user_survey.name
                                                }))

    except Survey.DoesNotExist:
        messages.error(request, "Wybrana ankieta nie istnieje.")
        return HttpResponseRedirect(reverse('home'))


@login_required
def answers(request, survey_id):
    kwargs = {}
    kwargs['answers'] = Answer.objects.filter(survey_id=survey_id).order_by('-created')
    return render(request, 'answers.html', kwargs)


@login_required
def delete_answer(request, survey_id, answer_id):
    try:
        survey_answer = Answer.objects.get(id=answer_id)
        survey_answer.delete()
        messages.success(request, "Wybrana odpowiedź została usunięta.")

    except Answer.DoesNotExist:
        messages.error(request, "Wybrane pytanie nie istnieje.")

    return HttpResponseRedirect(reverse('answers',
                                        kwargs={
                                            'survey_id': survey_id,
                                        }))


