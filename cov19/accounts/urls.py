from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView
from . import views


urlpatterns = [
    path('login/',LoginView.as_view(template_name='Reg/login.html'),name="Login"),
    path('register/',views.register,name="Register"),
    path('logout/',views.logout_view,name="Logout"),
    path('RDV/',views.Rdv,name="Rdv"),
    path('Rdv_management/',views.Rdv_management,name="Rdv_management"),
    path('Rdv_management/delete/<int:id>', views.delete),
    path('Rdv_management/accept/<int:id>', views.accept),
    path('profile/<int:id>',views.profile),


]

