# Generated by Django 4.0.4 on 2022-05-14 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_tracker', '0018_alter_testplan_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testplan',
            name='name',
            field=models.CharField(max_length=150),
        ),
    ]
