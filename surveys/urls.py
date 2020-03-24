from django.urls import path

from . import views

urlpatterns = [
    path('', views.surveys, name='surveys'),
    path('create/', views.create, name='create-survey'),
    path('<int:survey_id>/', views.survey, name='survey'),
    path('<int:survey_id>/delete/', views.delete, name='delete-survey'),

    path('<int:survey_id>/create-question/', views.create_question, name='create-question'),
    path('<int:survey_id>/delete-question/<int:question_id>/', views.delete_question, name='delete-question'),

    path('<int:survey_id>/share/<str:survey_name>/', views.share, name='share-survey'),
    path('<int:survey_id>/answers/', views.answers, name='answers'),
    path('<int:survey_id>/answer/<int:answer_id>/delete/', views.delete_answer, name='delete-answer'),
]
