from django.contrib.auth.models import User
from django.db.backends import sqlite3
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from datetime import datetime

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser

from . import serializers

from .models import Group, Event, Profile, Member, Comment, Bet


class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = serializers.UserSerializer
  authentication_classes = (TokenAuthentication,)
  permission_classes = (AllowAny,)

  # Acepte uniquement urls les terminees par '<int>:pk/change_pass/'. eg: "http://127.0.0.1:8000/api/user/18/change_pass/"
  # Voir urls.py "router.register(r'sigin', views.UserViewSet)"
  @action(methods=['PUT'], detail=True, serializer_class=serializers.ChangePasswordSerializer, permission_classes=[IsAuthenticated])
  def change_pass(self, request, pk):
    user = User.objects.get(pk=pk)
    serializer = serializers.ChangePasswordSerializer(data=request.data)

    if serializer.is_valid():

      if not user.check_password(serializer.data.get('old_password')):
        return Response({'message': 'Wrong password'}, status.HTTP_400_BAD_REQUEST)

      # print(">>>>>User", user, "<<<<<<")
      user.set_password(serializer.data.get('new_password'))
      user.save()
      return Response({'message': 'Password updated'}, status.HTTP_200_OK)


class CommentViewSet(viewsets.ModelViewSet):
  queryset = Comment.objects.all()
  serializer_class = serializers.CommentSerializer
  authentication_classes = (TokenAuthentication,)
  permission_classes = (IsAuthenticated,)


class ProfileViewSet(viewsets.ModelViewSet):
  queryset = Profile.objects.all()
  serializer_class = serializers.ProfileSerializer
  authentication_classes = (TokenAuthentication,)
  permission_classes = (IsAuthenticated,)


class GroupViewSet(viewsets.ModelViewSet):
  queryset = Group.objects.all()
  serializer_class = serializers.GroupSerializer
  authentication_classes = (TokenAuthentication,)
  permission_classes = (IsAuthenticatedOrReadOnly,)


  def retrieve(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = serializers.GroupFullSerializer(instance, many=False, context={'required': request})
    return Response(serializer.data)


class EventViewSet(viewsets.ModelViewSet):
  queryset = Event.objects.all()
  serializer_class = serializers.EventSerializer
  authentication_classes = (TokenAuthentication,)
  permission_classes = (IsAuthenticated,)

  def retrieve(self, request, *args, **kwargs):
    instance = self.get_object()
    # print("Instance >>>>>>>>>>>>", instance.time, "<<<<<<<<<<<<")
    serializer = serializers.EventFullSerializer(instance, many=False, context={'required': request})
    return Response(serializer.data)


class MemberViewSet(viewsets.ModelViewSet):
  queryset = Member.objects.all()
  serializer_class = serializers.MemberSerializer
  authentication_classes = (TokenAuthentication,)
  permission_classes = (AllowAny,)

  @action(methods=['POST'], detail=False)
  def join(self, request):
    if 'group' and 'user' in request.data:

      try:
        group = Group.objects.get(id=request.data['group'])
        user = User.objects.get(id=request.data['user'])
        member = Member.objects.create(user=user, group=group, admin=False)
        serializer = serializers.MemberSerializer(member, many=False)
        response = {'message': 'Joined Group', 'resultat': serializer.data}
        return Response(response, status=status.HTTP_200_OK)
      except:
        response = {'message': 'Cannot join'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    else:
      response = {'message': 'Wrong params'}
      return Response(response, status=status.HTTP_400_BAD_REQUEST)

  @action(methods=['POST'], detail=False)
  def leave(self, request):
    if 'group' and 'user' in request.data:

      try:
        group = Group.objects.get(id=request.data['group'])
        user = User.objects.get(id=request.data['user'])
        member = Member.objects.get(user=user, group=group)
        member.delete()
        response = {'message': 'Left Group'}
        return Response(response, status=status.HTTP_200_OK)
      except:
        response = {'message': 'Cannot leave group'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    else:
      response = {'message': 'Wrong params'}
      return Response(response, status=status.HTTP_400_BAD_REQUEST)


class BetViewSet(viewsets.ModelViewSet):
  queryset = Bet.objects.all()
  serializer_class = serializers.BetSerializer
  authentication_classes = (TokenAuthentication,)
  permission_classes = (IsAuthenticated,)

  @action(methods=['POST'], detail=False, url_path='place_bet')
  def place_bet(self, request):
    print("User>>>>>", request.user)
    if 'event' in request.data and 'score1' in request.data and 'score2' in request.data:

      event = Event.objects.get(id=request.data['event'])
      in_group = self.checkIfUserInGroup(event, request.user)

      if in_group: # event.time > datetime.now() and
        score1 = request.data['score1']
        score2 = request.data['score2']

        try:
          # UPDATE Senario
          my_bet = Bet.objects.get(event=event, user=request.user)
          my_bet.score1 = score1
          my_bet.score2 = score2
          my_bet.save()
          serializer = serializers.BetSerializer(my_bet, many=False)
          response = {'message': 'bet updated', 'new': False, 'result': serializer.data}
          return Response(response, status=status.HTTP_200_OK)

        except:
          # CREATE Senario
          bet = Bet.objects.create(user=request.user, event=event, score1=score1, score2=score2)
          serializer = serializers.BetSerializer(bet, many=False)
          response = {'message': 'bet updated', 'new': True, 'result': serializer.data}
          return Response(response, status=status.HTTP_200_OK)

      else:
        response = {'message': 'Cannot place bet. Too late!'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    else:
      response = {'message': 'Wrong params'}
      return Response(response, status=status.HTTP_400_BAD_REQUEST)

  def checkIfUserInGroup(self, event, user):
    try:
      return Member.objects.get(group=event.group, user=user)
    except:
      return False

  """
  @action(methods=['POST'], detail=False, url_path='place_bet')
  def place_bet(self, request):
    print(request.data['event'], request.data['user'])
    if 'user' and 'event' in request.data:
      try:
        event = Event.objects.get(id=request.data['event'])
        user = User.objects.get(id=request.data['user'])
        bet = Bet.objects.create(user=user, event=event, score1=request.data['score1'], score2=request.data['score2'])
        serializer = serializers.BetSerializer(bet, many=False)
        response = serializer.data
        print('serializer>>>>>>', response)
        return Response(response, status=status.HTTP_200_OK)
      except:
        response = {'message': 'Cannot place bet'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    else:
      response = {'message': 'Wrong params'}
      return Response(response, status=status.HTTP_400_BAD_REQUEST)
    """


class CustomObtainAuthToken(ObtainAuthToken):
  def post(self, request, *args, **kwargs):
    response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
    token = Token.objects.get(key=response.data['token'])
    user = User.objects.get(id=token.user_id)
    serializer = serializers.UserSerializer(user, many=False)
    return Response({'token': token.key, 'user': serializer.data})