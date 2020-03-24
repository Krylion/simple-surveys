from django.urls import path

from . import views

urlpatterns = [
    path('', views.notifications, name='notifications'),
    path('<int:notification_id>/delete/', views.delete, name='delete-notification'),
    path('set-as-read/', views.set_as_read, name='set-as-read'),
]
