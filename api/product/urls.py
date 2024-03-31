from django.urls import path

from . import views

urlpatterns = [
    path('getinfo/', views.GeneralInfo.as_view(), name='ginfo'),
    path('list/', views.ProductFilter.as_view(), name='list'),
    path('combo-list/', views.ComboFilter.as_view(), name='combo-list'),
]