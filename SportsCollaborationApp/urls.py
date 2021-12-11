from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.mainPage, name="main"),
    path('login/',views.loginPage, name="login"),
    path('signup/',views.registerPage, name="register"),
    path('logout/', views.logoutPage, name="logout"),
    path('profile/<str:username>/', views.profilePage, name="profile"),
    path('settings/', views.settingsPage, name="settings"),
    path('search/<str:search_str>/', views.searchPage, name="search"),
    path('activity/<str:id>/', views.activityPage, name="activity"),
    path('requestActivity/<str:id>/', views.requestActivity, name="request_activity"),
    path('finishActivity/<str:id>/', views.finishActivity, name="finish_activity"),
    path('postActivity/', views.postActivityPage, name="post_activity"),
    path('settings/changePassword/', views.changePasswordPage, name="change_password"),
    path('freezeAccount/', views.freezeAccount, name="freeze_account"),
    path('notifications/', views.notificationsPage, name="notification"),
    path('acceptActivity/<str:id>/', views.acceptActivity, name="accept_activity"),
    path('deleteNotification/<str:id>/', views.deleteNotification, name="delete_notification"),
    path('rateActivity/<str:id>/<str:rating>/', views.rateActivity, name="rate_activity"),
    path('tutorMain/', views.tutorMainPage, name="tutor_main"),
    path('tutorSearch/<str:search_str>/', views.tutorSearchPage, name="tutor_search"),
    path('messages/', views.directMessagesPage, name="direct_messages"),
    path('messages/<str:user_id>/', views.privateMessagesPage, name="private_message"),
    path('startMessage/<str:user_id>/', views.startMessage, name="start_message"),
    path('postCourse/', views.postCoursePage, name="post_course"),
    path('course/<str:id>/', views.coursePage, name="course"),
    path('finishTutor/<str:id>/', views.finishTutor, name="finish_tutor"),
    path('rateTutor/<str:id>/<str:rating>/', views.rateTutor, name="rate_tutor"),
    path("password_reset/", views.passwordResetPage, name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='pages/PasswordResetDonePage.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='pages/PasswordResetConfirmPage.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='pages/PasswordResetCompletePage.html'), name='password_reset_complete'),
    path('paymentScreenPage/<str:tutor_id>/<str:user_id>/', views.paymentScreenPage, name="payment_screen"),
    path('paymentResultPage/<str:tutor_id>/<str:user_id>/', views.paymentResultPage, name="payment_result")
]