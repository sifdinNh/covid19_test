from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Home, name='Home'),
    path('user/',include('accounts.urls')),

]