from django.urls import path

from . import views

urlpatterns = [
    path('init', views.GoogleCalendarInitView, name='GoogleCalendarInitView'),
    path('redirect', views.GoogleCalendarRedirectView,name='GoogleCalendarRedirectView')
]