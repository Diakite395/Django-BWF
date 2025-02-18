# Generated by Django 5.1.3 on 2025-01-19 00:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_comment'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score1', models.IntegerField(blank=True, null=True)),
                ('score2', models.IntegerField(blank=True, null=True)),
                ('points', models.IntegerField(blank=True, default=None, null=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bet', to='api.event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_bet', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'event')},
            },
        ),
    ]
