# Generated by Django 3.2.6 on 2021-12-08 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SportsCollaborationApp', '0021_auto_20211208_0913'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tutorshipmodel',
            name='tutorshipStatus',
        ),
        migrations.AlterField(
            model_name='tutor',
            name='tutoringStatus',
            field=models.CharField(choices=[('1', 'Ongoing'), ('2', 'Full'), ('3', 'Completed')], max_length=25),
        ),
    ]
