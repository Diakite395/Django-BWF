from . import views
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import include, re_path


router = routers.DefaultRouter()
router.register(r'groups', views.GroupViewSet)
router.register(r'events', views.EventViewSet)
router.register(r'members', views.MemberViewSet, basename='members')
router.register(r'comment', views.CommentViewSet)
router.register(r'user', views.UserViewSet)
router.register(r'profile', views.ProfileViewSet)
router.register(r'bets', views.BetViewSet)

urlpatterns = [
  re_path(r'^', include(router.urls)),
  re_path(r'authenticate/', views.CustomObtainAuthToken.as_view()),
]