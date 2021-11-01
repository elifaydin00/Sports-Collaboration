from django.urls import path
from . import views

urlpatterns = [
  path('', views.mainPage, name="main"),
  path('login',views.LoginPage, name="login"),
]