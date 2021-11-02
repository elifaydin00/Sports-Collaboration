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

    email = request.POST['email']
    password = request.POST['password']

    try:
      user = SiteUser.objects.get(email=email)
    except:
      messages.error(request, 'User does not exist!')
      return redirect('login')

    user = auth.authenticate(request, username=email.split("@")[0], password=password)

    if user is not None:
      auth.login(request, user)
      return redirect('main')
    else:
      messages.error(request, 'Email or password is incorrect!')
      return redirect('login')

  return render(request, "pages/LoginPage.html")

def logoutPage(request):
  auth.logout(request)
  return redirect('login')

@login_required(login_url='login')
def mainPage(request):
  return render(request, 'pages/MainPage.html')