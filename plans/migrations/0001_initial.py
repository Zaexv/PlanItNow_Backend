# Generated by Django 3.1.4 on 2021-09-03 19:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('userprofiles', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('english_title', models.CharField(default='pending translation', max_length=256)),
                ('description', models.CharField(max_length=1024)),
                ('english_description', models.CharField(default='pending translation', max_length=1024)),
                ('location', models.CharField(max_length=128)),
                ('init_date', models.DateField()),
                ('init_hour', models.TimeField()),
                ('end_hour', models.TimeField()),
                ('is_public', models.BooleanField(null=True)),
                ('max_participants', models.IntegerField(blank=True, default=5, null=True)),
                ('url_plan_picture', models.CharField(max_length=512, null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('init_date', 'init_hour', 'end_hour'),
            },
        ),
        migrations.CreateModel(
            name='PlanParticipation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user_likes', models.BooleanField(default=True)),
                ('participant_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participant_user', to='userprofiles.userprofile')),
                ('participating_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participating_plan', to='plans.plan')),
            ],
        ),
    ]
