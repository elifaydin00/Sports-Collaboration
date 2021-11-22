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

def registerPage(request):

    if request.user.is_authenticated:
        return redirect('main')

    if request.method == 'POST':

        name = request.POST['fullname']
        email = request.POST['email']
        age = request.POST['age']
        number = request.POST['number']
        gender = request.POST['gender']
        location = request.POST['location']
        password = request.POST['password']
        password2 = request.POST['password2']

        if (name == "" or gender == "Please select" or password == "" or number == "" or email == "" or password2 == "" or age == "" or location == ""):
            messages.error(request, 'Please, fill all of fields!')
            return redirect('register')

        try:
            user = SiteUser.objects.get(email=email)
            messages.error(request, 'Email is already registered!')
            return redirect('register')
        except:
            pass

        if int(age) < 15 or int(age) > 55:
            messages.error(request, 'Your age is not eligible to sign up!')
            return redirect('register')

        try:
            user = SiteUser.objects.get(phoneNumber=number)
            messages.error(request, 'Phone number is already registered!')
            return redirect('register')
        except:
            pass
        
        if password != password2:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')

        gender_val = '0'
        if gender == "Male":
            gender_val = '1'
        elif gender == "Female":
            gender_val = '2'
        elif gender == "Other":
            gender_val = '3'

        user = User.objects.create_user(email.split("@")[0], '', password)
        siteUser = SiteUser(user=user, name=name, email=email, age=age, phoneNumber=number, gender=gender_val, location=location, balance=0.0)
        siteUser.save()
        auth.login(request, user)
        return redirect('main')

    return render(request, 'pages/RegisterPage.html')

def logoutPage(request):
    auth.logout(request)
    return redirect('login')

@login_required(login_url='login')
def mainPage(request):
    participated_activities = ParticipantOfActivity.objects.filter(siteUser__user=request.user)
    activities = []
    tags_list = []
    for i in participated_activities:
        if i.activity.status != '3':
            curr_tags = Tag.objects.filter(activity=i.activity)
            curr_tags_strings_list = []
            for j in curr_tags:
                curr_tags_strings_list.append(j.descriptiveString)
            curr_tags_strings_list.sort()
            activities.append(i.activity)
            tags_list.append(curr_tags_strings_list)


    if request.method == 'POST':
        if request.POST.get('search_box') != "":
            return redirect('search', request.POST.get('search_box'))
        else:
            messages.error(request, "Search field can not be empty!")

    return render(request, 'pages/MainPage.html', {'activities_tags': zip(activities, tags_list), 'exist': len(activities) != 0})

@login_required(login_url='login')
def profilePage(request, username):
    user = User.objects.get(username=username)
    siteUser = SiteUser.objects.get(user=user)
    participated_activities = ParticipantOfActivity.objects.filter(siteUser__user=request.user)
    activities = []
    tags_list = []
    for i in participated_activities:
        if i.activity.status == '3':
            curr_tags = Tag.objects.filter(activity=i.activity)
            curr_tags_strings_list = []
            for j in curr_tags:
                curr_tags_strings_list.append(j.descriptiveString)
            curr_tags_strings_list.sort()
            activities.append(i.activity)
            tags_list.append(curr_tags_strings_list)
    return render(request, 'pages/ProfilePage.html', {'siteUser': siteUser, 'itself': request.user == user, 'activities_tags': zip(activities, tags_list)})

@login_required(login_url='login')
def settingsPage(request):
    return render(request, 'pages/SettingsPage.html')

@login_required(login_url='login')
def searchPage(request, search_str):

	all_activities = list(Activity.objects.all())
	all_activities.sort(key = lambda x : x.title)
	all_tags = Tag.objects.all()
	activities = []
	tags_list = []
	if search_str[0] != "#":
		for i in all_activities:
			if i.status != '3' and (search_str.lower() in i.title.lower() or search_str.lower() in i.siteUser.name.lower()):
				curr_tags = Tag.objects.filter(activity=i)
				curr_tags_strings_list = []
				for j in curr_tags:
					curr_tags_strings_list.append(j.descriptiveString)
				curr_tags_strings_list.sort()
				activities.append(i)
				tags_list.append(curr_tags_strings_list)
	else:
		for i in all_tags:
			if i.activity not in activities and i.activity.status != 3 and search_str.lower() in i.descriptiveString.lower():
				curr_tags = Tag.objects.filter(activity=i.activity)
				curr_tags_strings_list = []
				for j in curr_tags:
					curr_tags_strings_list.append(j.descriptiveString)
				curr_tags_strings_list.sort()
				activities.append(i.activity)
				tags_list.append(curr_tags_strings_list)

	return render(request, 'pages/SearchPage.html', {'activities_tags': zip(activities, tags_list), 'exist': len(activities) != 0})

@login_required(login_url='login')
def activityPage(request, id):
	siteUser = SiteUser.objects.get(user=request.user)
	activity = Activity.objects.get(id=id)
	tags = Tag.objects.filter(activity=activity)
	participants = ParticipantOfActivity.objects.filter(activity=activity)
	joined = False
	for i in list(participants):
		if i.siteUser == siteUser:
			joined = True
			break
	return render(request, 'pages/ActivityPage.html', {'activity': activity, 'tags': tags, 'joined': joined})

@login_required(login_url='login')
def participateActivity(request, id):
	activity = Activity.objects.get(id=id)
	if (activity.currentUsers == activity.maxUsers):
		return redirect('activity', id)
	siteUser = SiteUser.objects.get(user=request.user)
	participants = ParticipantOfActivity.objects.filter(activity=activity, siteUser=siteUser)
	if len(participants) == 1:
		return redirect('activity', id)
	newParticipant = ParticipantOfActivity(siteUser=siteUser, activity=activity)
	activity.currentUsers += 1
	if activity.currentUsers == activity.maxUsers:
		activity.status = '2'
	newParticipant.save()
	activity.save()
	return redirect('activity', id)