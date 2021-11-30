# Generated by Django 3.2.6 on 2021-11-29 22:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SportsCollaborationApp', '0006_auto_20211129_2227'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ActivityReview',
            new_name='ActivityRating',
        ),
        migrations.RenameModel(
            old_name='TutorshipReview',
            new_name='TutorRating',
        ),
        migrations.RemoveField(
            model_name='userskillreview',
            name='activity',
        ),
        migrations.RemoveField(
            model_name='userskillreview',
            name='attendantUser',
        ),
        migrations.RemoveField(
            model_name='userskillreview',
            name='reviewedUser',
        ),
        migrations.DeleteModel(
            name='Skill',
        ),
        migrations.DeleteModel(
            name='UserSkillReview',
        ),
    ]