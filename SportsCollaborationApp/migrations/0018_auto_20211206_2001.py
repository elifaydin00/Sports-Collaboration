# Generated by Django 3.2.6 on 2021-12-06 17:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SportsCollaborationApp', '0017_remove_tutorshipmodel_tutorshipstatus'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tutorrating',
            name='tutor',
        ),
        migrations.AddField(
            model_name='tutorrating',
            name='tutorName',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tutorUser', to='SportsCollaborationApp.siteuser'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tutorrating',
            name='siteUser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='raterUser', to='SportsCollaborationApp.siteuser'),
        ),
    ]
