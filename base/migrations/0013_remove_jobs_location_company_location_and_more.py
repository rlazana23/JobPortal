# Generated by Django 4.0.1 on 2022-01-31 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_jobs_jobapplication'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobs',
            name='location',
        ),
        migrations.AddField(
            model_name='company',
            name='location',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='jobs',
            name='ispart_time',
            field=models.BooleanField(default=False),
        ),
    ]
