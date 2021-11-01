from django.shortcuts import render

def mainPage(request):
  return render(request, 'pages/main.html')

def LoginPage(request):
  return render(request, "pages/login.html")