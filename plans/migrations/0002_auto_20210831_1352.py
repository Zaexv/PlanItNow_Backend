# Generated by Django 3.1.4 on 2021-08-31 13:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('userprofiles', '__first__'),
        ('plans', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='plan',
            options={'ordering': ('init_date', 'init_hour', 'end_hour')},
        ),
        migrations.AddField(
            model_name='plan',
            name='max_participants',
            field=models.IntegerField(blank=True, default=5, null=True),
        ),
        migrations.AddField(
            model_name='plan',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='plan',
            name='url_plan_picture',
            field=models.CharField(max_length=512, null=True),
        ),
        migrations.AddField(
            model_name='planparticipation',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='planparticipation',
            name='participant_user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='participant_user', to='userprofiles.userprofile'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='planparticipation',
            name='participating_plan',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='participating_plan', to='plans.plan'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='planparticipation',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='planparticipation',
            name='user_likes',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='plan',
            name='is_public',
            field=models.BooleanField(null=True),
        ),
    ]