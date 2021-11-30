from django.shortcuts import redirect, render
from django.contrib import auth
from django.contrib.auth.models import User
from django.db.models import Q
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

        user = auth.authenticate(
            request, username=email.split("@")[0], password=password)

        if user is not None:
            siteUser = SiteUser.objects.get(user=user)
            siteUser.frozenAccount = False
            siteUser.save()
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

        if len(password) < 8 or len(password2) < 8:
            messages.error(
                request, 'Password length can not be less than 8 characters!')
            return redirect('register')

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
        siteUser = SiteUser(user=user, name=name, email=email, age=age,
                            phoneNumber=number, gender=gender_val, location=location, balance=0.0)
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
    rating_list = []
    for i in participated_activities:
        if i.activity.status != '3':
            activities.append(i.activity)
            
            curr_tags = Tag.objects.filter(activity=i.activity)
            curr_tags_strings_list = []
            for j in curr_tags:
                curr_tags_strings_list.append(j.descriptiveString)
            curr_tags_strings_list.sort()
            tags_list.append(curr_tags_strings_list)

            rating_list.append("Not finished yet")

    if request.method == 'POST':
        if request.POST.get('search_box') != "":
            return redirect('search', request.POST.get('search_box'))
        else:
            messages.error(request, "Search field can not be empty!")

    return render(request, 'pages/MainPage.html', {'activities_tags_ratings': zip(activities, tags_list, rating_list), 'exist': len(activities) != 0})


@login_required(login_url='login')
def profilePage(request, username):
    user = User.objects.get(username=username)
    siteUser = SiteUser.objects.get(user=user)
    allActivities = []
    participated_activities = ParticipantOfActivity.objects.filter(siteUser=siteUser)
    for i in participated_activities:
        allActivities.append(i.activity)
    activities = []
    tags_list = []
    rating_list = []
    count = ParticipantOfActivity.objects.filter(activity__status='3', siteUser=siteUser)
    for i in allActivities:
        if i.status == '3':
            activities.append(i)
            
            curr_tags = Tag.objects.filter(activity=i)
            curr_tags_strings_list = []
            for j in curr_tags:
                curr_tags_strings_list.append(j.descriptiveString)
            curr_tags_strings_list.sort()
            tags_list.append(curr_tags_strings_list)
            
            curr_ratings = ActivityRating.objects.filter(activity=i)
            point = 0
            counter = 0
            for j in curr_ratings:
                point += int(j.rating)
                counter += 1
            if counter == 0:
                rating_list.append("No ratings")
            else:
                rating_list.append(float("{:.2f}".format(point / float(counter))))

    return render(request, 'pages/ProfilePage.html', {'count': len(count), 'siteUser': siteUser, 'itself': request.user == user, 'activities_tags_ratings': zip(activities, tags_list, rating_list)})


@login_required(login_url='login')
def settingsPage(request):
    siteUser = SiteUser.objects.get(user=request.user)
    firstname = siteUser.name.split(" ")[0]
    lastname = siteUser.name.split(" ")[1]

    if request.method == 'POST':

        location = request.POST['location']
        age = request.POST['age']

        if location != "" and age != "":
            siteUser.location = location
            siteUser.age = int(age)
            siteUser.save()
        elif location == "" and age != "":
            siteUser.age = int(age)
            siteUser.save()
        elif location != "" and age == "":
            siteUser.location = location
            siteUser.save()

        return redirect('profile', request.user.username)

    return render(request, 'pages/SettingsPage.html', {'siteUser': siteUser, 'firstname': firstname, 'lastname': lastname})


@login_required(login_url='login')
def freezeAccount(request):
    siteUser = SiteUser.objects.get(user=request.user)
    participants = ParticipantOfActivity.objects.filter(siteUser=siteUser).filter(
        Q(activity__status='1') | Q(activity__status='2'))
    if (len(participants) != 0):
        messages.error(
            request, "You can not freeze your account while you have ongoing activities!")
        return redirect('settings')
    siteUser.frozenAccount = True
    siteUser.save()
    auth.logout(request)
    return redirect('login')


@login_required(login_url='login')
def changePasswordPage(request):

    if request.method == 'POST':

        enteredCurrentPwd = request.POST['currentPwd']
        enteredNewPwd = request.POST['newPwd']
        enteredNewPwdSec = request.POST['newPwdSec']

        user = auth.authenticate(
            request, username=request.user.username, password=enteredCurrentPwd)
        if enteredCurrentPwd == "" or enteredNewPwd == "" or enteredNewPwdSec == "":
            messages.error(request, "The blank(s) can not be empty!")
            return redirect('change_password')

        if user is None:
            messages.error(request, "Entered password is incorrect.")
            return redirect('change_password')

        if len(enteredNewPwd) < 8 or len(enteredNewPwdSec) < 8:
            messages.error(
                request, "Password length can not be less than 8 characters!")
            return redirect('change_password')

        if enteredNewPwd != enteredNewPwdSec:
            messages.error(request, "Passwords do not match!")
            return redirect('change_password')

        user = request.user
        user.set_password(enteredNewPwd)
        user.save()
        auth.login(request, user)

        return redirect('settings')

    return render(request, 'pages/ChangePasswordPage.html')


@login_required(login_url='login')
def searchPage(request, search_str):

    all_activities = list(Activity.objects.all())
    all_activities.sort(key=lambda x: x.title)
    all_tags = Tag.objects.all()
    activities = []
    tags_list = []
    rating_list = []
    if search_str[0] != "#":
        for i in all_activities:
            if i.status != '3' and (search_str.lower() in i.title.lower() or search_str.lower() in i.siteUser.name.lower()):
                activities.append(i)
                
                curr_tags = Tag.objects.filter(activity=i)
                curr_tags_strings_list = []
                for j in curr_tags:
                    curr_tags_strings_list.append(j.descriptiveString)
                curr_tags_strings_list.sort()
                tags_list.append(curr_tags_strings_list)

                rating_list.append("Not finished yet")
    else:
        for i in all_tags:
            if i.activity not in activities and i.activity.status != '3' and search_str.lower() in i.descriptiveString.lower():
                activities.append(i.activity)
                
                curr_tags = Tag.objects.filter(activity=i.activity)
                curr_tags_strings_list = []
                for j in curr_tags:
                    curr_tags_strings_list.append(j.descriptiveString)
                curr_tags_strings_list.sort()
                tags_list.append(curr_tags_strings_list)

                rating_list.append("Not finished yet")


    return render(request, 'pages/SearchPage.html', {'activities_tags_ratings': zip(activities, tags_list, rating_list), 'exist': len(activities) != 0})


@login_required(login_url='login')
def activityPage(request, id):
    siteUser = SiteUser.objects.get(user=request.user)
    activity = Activity.objects.get(id=id)
    tags = list(Tag.objects.filter(activity=activity))
    tags.sort(key=lambda x: x.descriptiveString)
    joinStatus = 2
    participant = ParticipantOfActivity.objects.filter(activity=activity, siteUser=siteUser)
    if len(participant) != 0:
        joinStatus = 1
    applicant = ApplicantOfActivity.objects.filter(activity=activity, siteUser=siteUser)
    if len(applicant) != 0:
        joinStatus = 0
    
    rating = "Not finished yet"
    curr_ratings = ActivityRating.objects.filter(activity=activity)
    point = 0
    counter = 0
    for j in curr_ratings:
        point += int(j.rating)
        counter += 1
    if counter == 0:
        rating = "No ratings"
    else:
        rating = float("{:.2f}".format(point / float(counter)))

    return render(request, 'pages/ActivityPage.html', {'activity': activity, 'tags': tags, 'joinStatus': joinStatus, 'owned': request.user == activity.siteUser.user, 'rating': rating})


@login_required(login_url='login')
def requestActivity(request, id):
    activity = Activity.objects.get(id=id)
    if (activity.currentUsers == activity.maxUsers):
        return redirect('activity', id)
    siteUser = SiteUser.objects.get(user=request.user)
    alreadyRequested = ApplicantOfActivity.objects.filter(activity=activity, siteUser=siteUser)
    if len(alreadyRequested) == 1:
        return redirect('activity', id)
    title = "Joining Activity Request"
    description = siteUser.name + " wants to join your activity '" + activity.title + "'."
    newNotifi = Notification(senderSiteUser=siteUser, receiverSiteUser=activity.siteUser, title=title, description=description, notificationType='2')
    newNotifi.save()
    newApplicant = ApplicantOfActivity(siteUser=siteUser, activity=activity, notification=newNotifi)
    newApplicant.save()
    return redirect('activity', id)


@login_required(login_url='login')
def finishActivity(request, id):
    activity = Activity.objects.get(id=id)
    if (activity.siteUser.user != request.user):
        return redirect('activity', id)
    activity.status = '3'
    activity.save()
    siteUser = SiteUser.objects.get(user=request.user)
    participants = ParticipantOfActivity.objects.exclude(siteUser=siteUser).filter(activity=activity)
    for i in participants:
      title = "Rating Finished Activity"
      description = "Please rate the activity '" + activity.title + "'."
      newNotifi = Notification(senderSiteUser=siteUser, receiverSiteUser=i.siteUser, title=title, description=description, pointerId=id, notificationType='3')
      newNotifi.save()
    return redirect('activity', id)


@login_required(login_url='login')
def postActivityPage(request):

    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        max_users = request.POST['max_users']
        tags = request.POST['tags'].split()

        if title == "" or description == "" or max_users == "":
            messages.error(request, 'Please, fill all of fields!')
            return redirect('post_activity')

        if len(title) < 10:
            messages.error(request, 'Activity title field must have 10 or more characters!')
            return redirect('post_activity')

        if len(description) < 25:
            messages.error(request, 'Activity description field must have 25 or more characters!')
            return redirect('post_activity')

        if int(max_users) < 2:
            messages.error(request, 'Maximum participants field must be larger than 1!')
            return redirect('post_activity')

        siteUser = SiteUser.objects.get(user=request.user)
        newActivity = Activity(siteUser=siteUser, title=title, description=description,status='1', currentUsers=1, maxUsers=int(max_users))
        newActivity.save()
        newParticipant = ParticipantOfActivity(siteUser=siteUser, activity=newActivity)
        newParticipant.save()

        if len(tags) != 0:
            for i in tags:
                newTag = Tag(activity=newActivity, descriptiveString="#"+i)
                newTag.save()

        return redirect('main')

    return render(request, 'pages/PostActivityPage.html')


@login_required(login_url='login')
def notificationsPage(request):
    siteUser = SiteUser.objects.get(user=request.user)
    notifications = list(Notification.objects.filter(receiverSiteUser=siteUser))
    notifications.sort(key=lambda x: x.title)
    return render(request, 'pages/NotificationsPage.html', {'notifications': notifications, 'exist': len(notifications) != 0})


@login_required(login_url='login')
def acceptActivity(request, id):
    notification = Notification.objects.get(id=id)
    requestedSiteUser = notification.senderSiteUser
    targetSiteUser = notification.receiverSiteUser
    if request.user != targetSiteUser.user:
        return redirect('notification')
    applicant = ApplicantOfActivity.objects.get(notification=notification, siteUser=requestedSiteUser)
    activity = applicant.activity
    newParticipant = ParticipantOfActivity(siteUser=requestedSiteUser, activity=activity)
    applicant.delete()
    newParticipant.save()
    activity.currentUsers += 1
    if activity.currentUsers == activity.maxUsers:
        activity.status = '2'
    activity.save()
    notification.delete()
    title = "About " + targetSiteUser.name + "'s Activity"
    description = "You have been accepted to the activity '" + activity.title + "'."
    newNotifi = Notification(senderSiteUser=targetSiteUser, receiverSiteUser=requestedSiteUser, title=title, description=description, notificationType='1')
    newNotifi.save()
    if activity.currentUsers == activity.maxUsers:
        otherRequest = ApplicantOfActivity.objects.filter(activity=activity)
        otherRequestsNotifis = []
        for i in otherRequest:
            otherRequestsNotifis.append(i.notifications)
        for i in otherRequestsNotifis:
            i.delete()
    return redirect('notification')


@login_required(login_url='login')
def deleteNotification(request, id):
    notification = Notification.objects.get(id=id)
    requestedSiteUser = notification.senderSiteUser
    targetSiteUser = notification.receiverSiteUser
    if request.user != targetSiteUser.user:
        return redirect('notification')
    applicants = ApplicantOfActivity.objects.filter(notification=notification, siteUser=requestedSiteUser)
    if len(applicants) == 1:
        applicants[0].delete()
    notification.delete()
    return redirect('notification')


@login_required(login_url='login')
def rateActivity(request, id, rating):
    notification = Notification.objects.get(id=id)
    targetSiteUser = notification.receiverSiteUser
    if request.user != targetSiteUser.user:
        return redirect('notification')
    ratedActivity = Activity.objects.get(id=notification.pointerId)
    newRating = ActivityRating(attendantUser=targetSiteUser, activity=ratedActivity, rating=rating)
    newRating.save()
    notification.delete()
    return redirect('notification')