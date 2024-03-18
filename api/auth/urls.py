from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('register-mobile/', views.registerMobile, name="register-mobile"),
    path('sms-list/', views.smsList, name='sms-list'),
    path('user-detail/', views.userDetail, name='user-detail'),
]