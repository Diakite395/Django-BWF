from rest_framework.authtoken.models import Token
from rest_framework import serializers

from django.contrib.auth.models import User
from .models import Group, Event, Profile, Member, Comment, Bet


class ChangePasswordSerializer(serializers.Serializer):
  old_password = serializers.CharField(required=True)
  new_password = serializers.CharField(required=True)


class ProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = Profile
    fields = ['id', 'image', 'prenium', 'bio']


class UserSerializer(serializers.ModelSerializer):
  profile = ProfileSerializer(many=False)
  class Meta:
    model = User
    fields = ['id', 'username', 'email', 'password', 'profile']

    # Pour ne pas afficher le mot de pas dans le resultat
    extra_kwargs = {'password': {'write_only': True, 'required': False}}

  # voir la documentation 'Serializer relation/Writable nested serializers'
  def create(self, validated_data):
    # e.g: validated_data => {'username': 'Diakite1', 'email': 'test@gmail.com', 'password': 'pass', 'profile': {}}
    # print('Validate Data >>>>>>', validated_data)
    profile_data = validated_data.pop('profile')
    user = User.objects.create_user(**validated_data)
    Profile.objects.create(user=user, **profile_data)
    Token.objects.create(user=user)
    return user


class EventSerializer(serializers.ModelSerializer):
  class Meta:
    model = Event
    fields = ('id', 'team1', 'team2', 'time', 'group')

  def create(self, validated_data):
    # e.g: validated_data => {'username': 'Diakite1', 'email': 'test@gmail.com', 'password': 'pass', 'profile': {}}
    print('Validate Data >>>>>>', validated_data)
    event = Event.objects.create(**validated_data)
    return event


class BetSerializer(serializers.ModelSerializer):
  user = UserSerializer(many=False)
  class Meta:
    model = Bet
    fields = ('id', 'user', 'event', 'score1', 'score2', 'points')


class EventFullSerializer(serializers.ModelSerializer):
  bets = BetSerializer(many=True)
  class Meta:
    model = Event
    fields = ('id', 'team1', 'team2', 'time', 'score1', 'score2', 'group', 'bets')


class CommentSerializer(serializers.ModelSerializer):
  # user = UserSerializer(many=False)
  class Meta:
    model = Comment
    fields = ('user', 'group', 'description', 'time')


class MemberSerializer(serializers.ModelSerializer):
  user = UserSerializer(many=False)
  class Meta:
    model = Member
    fields = ('user', 'group', 'admin')


class GroupSerializer(serializers.ModelSerializer):
  class Meta:
    model = Group
    fields = ('id', 'name', 'location', 'description')


class GroupFullSerializer(serializers.ModelSerializer):
  events = EventSerializer(many=True)
  members = serializers.SerializerMethodField()
  comments = serializers.SerializerMethodField()

  class Meta:
    model = Group
    fields = ('id', 'name', 'location', 'description', 'events', 'members', 'comments')

  def get_comments(self, obj):
    comments = Comment.objects.filter(group=obj).order_by('time')
    serializer = CommentSerializer(comments, many=True)
    return serializer.data

  def get_members(self, obj):
    people_points = []
    # On tous les membres du group. Dans 'obj.members.all()' 'members' est le nom de la relation 'related_name'
    members = obj.members.all()
    for member in members:
      member_serializer = MemberSerializer(member, many=False)
      member_data = member_serializer.data
      points = 0
      member_data['points'] = points
      people_points.append(member_data)

    return people_points