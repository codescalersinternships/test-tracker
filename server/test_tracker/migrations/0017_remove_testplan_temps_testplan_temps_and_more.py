# Generated by Django 4.0.4 on 2022-05-14 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_tracker', '0016_testplan_temps'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testplan',
            name='temps',
        ),
        migrations.AddField(
            model_name='testplan',
            name='temps',
            field=models.JSONField(default=dict),
        ),
        migrations.DeleteModel(
            name='TestPlanDetail',
        ),
    ]