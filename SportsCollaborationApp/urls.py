from django.urls import path
from . import views

urlpatterns = [
  path('', views.mainPage, name="main"),
  path('login/',views.loginPage, name="login"),
  path('signup/',views.registerPage, name="register"),
  path('logout/', views.logoutPage, name="logout"),
  path('profile/<str:username>/', views.profilePage, name="profile"),
  path('settings/', views.settingsPage, name="settings")
]