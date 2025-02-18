from django.db import models
from django.contrib.auth.models import User


def upload_path_handler(instence, filename):
  return  f"avatars/{instence.user.id}/{filename}"


class Profile(models.Model):
  user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
  image = models.ImageField(upload_to=upload_path_handler, blank=True)
  prenium = models.BooleanField(default=False)
  bio = models.CharField(max_length=255, blank=True, null=True)


class Group(models.Model):
  name = models.CharField(max_length=32, null=False, unique=False)
  location = models.CharField(max_length=32, null=False)
  description = models.CharField(max_length=256, null=False, unique=False)

  def __str__(self):
    return self.name

  class Meta:
    unique_together = ['name', 'location']


class Event(models.Model):
  team1 = models.CharField(max_length=32, blank=False)
  team2 = models.CharField(max_length=32, blank=False)
  time = models.DateTimeField(null=False, blank=False)
  score1 = models.IntegerField(null=True, blank=True)
  score2 = models.IntegerField(null=True, blank=True)
  group = models.ForeignKey(Group, related_name='events', on_delete=models.CASCADE)


# Relation many To many entre Group et User
class Member(models.Model):
  group = models.ForeignKey(Group, related_name='members', on_delete=models.CASCADE)
  user = models.ForeignKey(User, related_name='member_of', on_delete=models.CASCADE)
  admin = models.BooleanField(default=False)

  class Meta:
    unique_together = ['user', 'group']
    # index_together = (('user', 'group'),)


class Comment(models.Model):
  group = models.ForeignKey(Group, related_name='comment', on_delete=models.CASCADE)
  user = models.ForeignKey(User, related_name='user_comment', on_delete=models.CASCADE)
  description = models.CharField(max_length=256, null=False, unique=False)
  time = models.DateTimeField(auto_now_add=True)


class Bet(models.Model):
  user = models.ForeignKey(User, related_name='user_bets', on_delete=models.CASCADE)
  event = models.ForeignKey(Event, related_name='bets', on_delete=models.CASCADE)
  score1 = models.IntegerField(null=True, blank=True)
  score2 = models.IntegerField(null=True, blank=True)
  points = models.IntegerField(default=None, null=True, blank=True)

  class Meta:
    unique_together = ['user', 'event']
