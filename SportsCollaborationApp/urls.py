from django.urls import path
from . import views

urlpatterns = [
  path('', views.mainPage, name="main"),
  path('login/',views.loginPage, name="login"),
  path('signup/',views.registerPage, name="register"),
  path('logout/', views.logoutPage, name="logout"),
  path('profile/<str:username>/', views.profilePage, name="profile"),
  path('settings/', views.settingsPage, name="settings"),
  path('search/<str:search_str>', views.searchPage, name="search"),
  path('activity/<str:id>', views.activityPage, name="activity"),
  path('participateActivity/<str:id>/', views.participateActivity, name="participate_activity"),
  path('finishActivity/<str:id>/', views.finishActivity, name="finish_activity"),
  path('postActivity/', views.postActivityPage, name="post_activity"),
  path('settings/changepassword/', views.changePassword, name="change_password"),
  
]