# Generated by Django 3.2.6 on 2021-12-06 15:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SportsCollaborationApp', '0015_delete_applicantoftutor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tutorrating',
            name='description',
        ),
        migrations.RemoveField(
            model_name='tutorrating',
            name='title',
        ),
    ]
