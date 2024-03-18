from django.urls import path

from . import views

urlpatterns = [
    path('info/', views.GeneralInfo.as_view(), name='info'),
]