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

class Skill(models.Model):
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	siteUser = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
	sport = models.CharField(max_length=100)
	rating = models.CharField(max_length=25, choices=(('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5)))

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

class ApplicantOfActivity(models.Model):
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	siteUser = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
	activity = models.ForeignKey(Activity, on_delete=models.CASCADE)

class ParticipantOfActivity(models.Model):
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	siteUser = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
	activity = models.ForeignKey(Activity, on_delete=models.CASCADE)

class ActivityReview(models.Model):
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	attendantUser = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
	activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
	title = models.CharField(max_length=100)
	description = models.TextField(max_length=500)
	rating = models.CharField(max_length=25, choices=(('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5)))

class UserSkillReview(models.Model):
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	attendantUser = models.ForeignKey(SiteUser, on_delete=models.CASCADE, related_name='attendantUser')
	reviewedUser = models.ForeignKey(SiteUser, on_delete=models.CASCADE, related_name='reviewedUser')
	activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
	title = models.CharField(max_length=100)
	description = models.TextField(max_length=500)
	rating = models.CharField(max_length=25, choices=(('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5)))

class Tutor(models.Model):
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	tutorName = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
	sport = models.CharField(max_length=50)
	description = models.TextField(max_length=500)
	tutoringStatus = models.CharField(max_length=25, choices=(('1', 'Available'), ('2', 'Not available')))

class ApplicantOfTutorship(models.Model):
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	siteUser = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
	tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)

class TutorshipModel(models.Model):
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)	
	siteUser = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
	tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
	tutorshipStatus = models.CharField(max_length=25, choices=(('1', 'In Progress'), ('2', 'Completed')))

class TutorshipReview(models.Model):
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)	
	siteUser = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
	tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
	title = models.CharField(max_length=100)
	description = models.TextField(max_length=500)
	rating = models.CharField(max_length=25, choices=(('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5)))

class Messages(models.Model):
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)	
	sourceUser = models.ForeignKey(SiteUser, on_delete=models.CASCADE, related_name='sourceUser')
	targetUser = models.ForeignKey(SiteUser, on_delete=models.CASCADE, related_name='targetUser')

class DirectMessage(models.Model):
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	message = models.ForeignKey(Messages, on_delete=models.CASCADE)
	text = models.TextField(max_length=500)
	time = models.TimeField()

class Notifications(models.Model):
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)	
	siteUser = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
	title = models.CharField(max_length=100)
	description = models.TextField(max_length=500)
	notificationStatus = models.CharField(max_length=25, choices=(('1', 'Sent Only'), ('2', 'Sent & Received')))