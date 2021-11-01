from django.shortcuts import redirect, render
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *

def loginPage(request):

  if request.user.is_authenticated:
    return redirect('main')

  if request.method == 'POST':

    error_given = False
    email = request.POST['email']
    password = request.POST['password']

    try:
      user = SiteUser.objects.get(email=email)

    except:
      if error_given is False:
        messages.error(request, 'User does not exist!')
        error_given = True

    user = auth.authenticate(request, username=email.split("@")[0], password=password)

    if user is not None:
      auth.login(request, user)
      return redirect('main')

    else:
      if error_given is False:
        messages.error(request, 'Email or password is incorrect!')
        error_given = True

  return render(request, "pages/LoginPage.html")

def logoutPage(request):
  auth.logout(request)
  return redirect('login')

@login_required(login_url='login')
def mainPage(request):
  return render(request, 'pages/MainPage.html')