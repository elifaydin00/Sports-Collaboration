from django.contrib import admin
from .models import *

admin.site.register(SiteUser)
admin.site.register(Skill)
admin.site.register(Activity)
admin.site.register(Tag)
admin.site.register(ApplicantOfActivity)
admin.site.register(ParticipantOfActivity)
admin.site.register(ActivityReview)
admin.site.register(UserSkillReview)
admin.site.register(Tutor)
admin.site.register(ApplicantOfTutorship)
admin.site.register(TutorshipModel)
admin.site.register(TutorshipReview)
admin.site.register(Messages)
admin.site.register(DirectMessage)
admin.site.register(Notifications)