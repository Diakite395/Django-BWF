# Generated by Django 5.1.3 on 2025-01-07 20:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_profile_bio_profile_prenium'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Meember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin', models.BooleanField(default=False)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='api.group')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member_of', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'group')},
            },
        ),
    ]
