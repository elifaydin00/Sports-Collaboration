# Generated by Django 3.2.6 on 2021-12-06 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SportsCollaborationApp', '0012_alter_directmessage_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='directmessage',
            name='owner',
            field=models.CharField(choices=[('1', 'Owner'), ('2', 'Not Owner')], default=1, max_length=25),
            preserve_default=False,
        ),
    ]
