from django.contrib import admin
from .models import Group, Event, Profile, Member, Comment, Bet


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
  fields = ('name', 'location', 'description')
  list_display = ('id', 'name', 'location', 'description')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
  fields = ('team1', 'team2', 'time', 'score1', 'score2', 'group')
  list_display = (('team1', 'team2', 'time', 'score1', 'score2', 'group'))


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
  fields = ('user', 'image', 'prenium', 'bio')
  list_display = ('id', 'user', 'image', 'prenium')


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
  fields = ('user', 'group', 'admin')
  list_display = ('id', 'user', 'group', 'admin')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
  fields = ('user', 'group', 'description')
  list_display = ('id', 'user', 'group', 'description', 'time')


@admin.register(Bet)
class BetAdmin(admin.ModelAdmin):
  fields = ('user', 'event', 'score1', 'score2', 'points')
  list_display = ('id', 'user', 'event', 'score1', 'score2', 'points')
