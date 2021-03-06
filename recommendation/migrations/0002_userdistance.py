# Generated by Django 3.1.4 on 2021-09-07 20:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userprofiles', '0001_initial'),
        ('plans', '0001_initial'),
        ('recommendation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDistance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('distance', models.FloatField(default=-1.0)),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plan_user_distance', to='plans.plan')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_distance', to='userprofiles.userprofile')),
            ],
        ),
    ]
