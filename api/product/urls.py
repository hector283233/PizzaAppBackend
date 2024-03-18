from django.urls import path

from . import views

urlpatterns = [
    path('ginfo/', views.GeneralInfo.as_view(), name='ginfo'),
    path('list/', views.ProductFilter.as_view(), name='list'),
]