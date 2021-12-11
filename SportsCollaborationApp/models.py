from django.db import models
from django.contrib.auth.models import User
import uuid

class SiteUser(models.Model):
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=50)
	email = models.CharField(max_length=50)
	age = models.IntegerField()
	gender = models.CharField(max_length=25, choices=(('1', 'Male'), ('2', 'Female'), ('3', 'Other')))
	location = models.CharField(max_length=150)
	phoneNumber = models.CharField(max_length=25)
	balance = models.FloatField()
	frozenAccount = models.BooleanField(default=False)

class Activity(models.Model):
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	siteUser = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
	title = models.CharField(max_length=100)
	description = models.TextField(max_length=500)
	status = models.CharField(max_length=25, choices=(('1', 'Activity is available to join!'), ('2', 'Activity is in progress!'), ('3', 'Activity ended!')))
	currentUsers = models.IntegerField()
	maxUsers = models.IntegerField()

class Tag(models.Model):
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
	descriptiveString = models.CharField(max_length=50)

class ParticipantOfActivity(models.Model):
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	siteUser = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
	activity = models.ForeignKey(Activity, on_delete=models.CASCADE)

class ActivityRating(models.Model):
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	attendantUser = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
	activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
	rating = models.CharField(max_length=25, choices=(('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5)))

class Tutor(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    tutorName = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    tutoringStatus = models.CharField(max_length=25, choices=(('1', 'Ongoing'), ('2', 'Full'), ('3', 'Completed')))
    totalFee = models.CharField(max_length=10)
    currentUsers = models.IntegerField()
    maxUsers = models.IntegerField()

class TutorshipModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)	
    siteUser = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)

class TutorRating(models.Model):
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)	
	siteUser = models.ForeignKey(SiteUser, on_delete=models.CASCADE, related_name='raterUser')
	tutorName = models.ForeignKey(SiteUser, on_delete=models.CASCADE, related_name='tutorUser')
	rating = models.CharField(max_length=25, choices=(('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5)))

class Message(models.Model):
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)	
	sourceUser = models.ForeignKey(SiteUser, on_delete=models.CASCADE, related_name='sourceUser')
	targetUser = models.ForeignKey(SiteUser, on_delete=models.CASCADE, related_name='targetUser')

class DirectMessage(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    time = models.TimeField(auto_now_add=True)

class Notification(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    senderSiteUser = models.ForeignKey(SiteUser, on_delete=models.CASCADE, related_name='senderUser')
    receiverSiteUser = models.ForeignKey(SiteUser, on_delete=models.CASCADE, related_name='receiverUser')
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    pointerId = models.CharField(max_length=50, null=True, blank=True)
    notificationType = models.CharField(max_length=25, choices=(('1', 'Acknowledgement'), ('2', 'Request'), ('3', 'RatingActivity'), ('4', 'RatingTutor')))

class ApplicantOfActivity(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    siteUser = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)