# Generated by Django 4.0.4 on 2022-05-13 23:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('test_tracker', '0013_people_signature'),
    ]

    operations = [
        migrations.AlterField(
            model_name='people',
            name='signature',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='test_tracker.invitesignature'),
        ),
    ]