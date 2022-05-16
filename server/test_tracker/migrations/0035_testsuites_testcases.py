# Generated by Django 4.0.4 on 2022-05-16 06:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('test_tracker', '0034_alter_requirements_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestSuites',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=150)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_test_suites', to='test_tracker.project')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TestCases',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField(default='')),
                ('test_steps', models.TextField(default='A list of steps to perform along with any sample data.')),
                ('expected_result', models.TextField(default='Details of what the final result should be.')),
                ('verifies_requirements', models.ManyToManyField(related_name='verifies_requirements', to='test_tracker.requirements')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
