# Generated by Django 3.2.6 on 2021-11-29 18:31

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('SportsCollaborationApp', '0002_alter_siteuser_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notifications',
            name='notificationStatus',
        ),
        migrations.AddField(
            model_name='notifications',
            name='notificationType',
            field=models.CharField(choices=[('1', 'Acknowledgement'), ('2', 'Request')], default=1, max_length=25),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='TutorRequests',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('requestedSiteUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SportsCollaborationApp.siteuser')),
                ('tutor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SportsCollaborationApp.tutor')),
            ],
        ),
        migrations.CreateModel(
            name='ActivityRequests',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SportsCollaborationApp.activity')),
                ('requestedSiteUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SportsCollaborationApp.siteuser')),
            ],
        ),
    ]
