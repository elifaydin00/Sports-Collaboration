from django.contrib import admin
from .models import *

admin.site.register(SiteUser)
admin.site.register(Activity)
admin.site.register(Tag)
admin.site.register(ApplicantOfActivity)
admin.site.register(ParticipantOfActivity)
admin.site.register(ActivityRating)
admin.site.register(Tutor)
admin.site.register(ApplicantOfTutor)
admin.site.register(TutorshipModel)
admin.site.register(TutorRating)
admin.site.register(Message)
admin.site.register(DirectMessage)
admin.site.register(Notification)