from rest_framework.routers import DefaultRouter
from django.urls import path,include


from userprofile.views import UserProfileViewSet , GoogleAuthAPIView, UserViewSet,profile_completed

router = DefaultRouter()
router.register('user-profile',UserProfileViewSet,basename='userprofile')
router.register('user-details',UserViewSet,basename='user-details')

urlpatterns = [
    path('',include(router.urls)),
    path('auth/login/google/',GoogleAuthAPIView.as_view(),name='google-auth-connect'),
    path('/profile-completed',profile_completed,name="profile-completed")

]


