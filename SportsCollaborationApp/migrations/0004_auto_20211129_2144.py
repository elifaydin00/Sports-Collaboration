# Generated by Django 3.2.6 on 2021-11-29 18:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SportsCollaborationApp', '0003_auto_20211129_2131'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tutorrequests',
            name='requestedSiteUser',
        ),
        migrations.RemoveField(
            model_name='tutorrequests',
            name='tutor',
        ),
        migrations.DeleteModel(
            name='ActivityRequests',
        ),
        migrations.DeleteModel(
            name='TutorRequests',
        ),
    ]