from sys import path

from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from urllib.parse import urlencode

from django_filters.rest_framework import DjangoFilterBackend
from key_value.aio.wrappers import retry
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from crm_backend import settings
from rest_framework import viewsets

from userprofile.filters import UserFilter
from userprofile.serializer import UserProfileSerializer,GoogleAuthSerializer, UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
import requests
from django.contrib.auth.models import User
from userprofile.models import UserProfile




# Create your views here.



class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    """Make the interogation : UserProfile.objects.get(user_id=1)"""
    lookup_field = 'user'


class GoogleAuthAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self,request):
        serializer = GoogleAuthSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data.get('code')
        error = serializer.validated_data.get('error')

        login_url = f'{settings.FRONTEND_URL}/login'

        if error or not code:
            params = urlencode({'error': error or 'no_code'})
            return redirect(f'{login_url}?{params}')

        # Change the code for accest_token
        token_response = requests.post(
            'https://oauth2.googleapis.com/token',
            data={
                'code':code,
                'client_id':settings.GOOGLE_OAUTH_CLIENT_ID,
                'client_secret':settings.GOOGLE_OAUTH_CLIENT_SECRET,
                'redirect_uri': f'{settings.BACKEND_URL}/api/v1/auth/login/google/',
                'grant_type': 'authorization_code',
            },
            timeout=10
        )

        if not token_response.ok:
            print('=== TOKEN EXCHANGE FAILED===')
            print('Status: ', token_response.status_code)
            print('Response: ', token_response.text)
            print('Sent data: ', {
                'code':code[:20] + "...", #first 20 from code
                'client_id':settings.GOOGLE_OAUTH_CLIENT_ID,
                'redirect_uri': f'{settings.BACKEND_URL}/api/v1/auth/login/google/',
                'grant_type':'authorization_code',

            })
            return redirect(f'{login_url}?error=token_exchange_failed')

        access_token = token_response.json().get('access_token')

        userinfo_response = requests.get(
            'https://www.googleapis.com/oauth2/v3/userinfo',
            headers={'Authorization':f'Bearer {access_token}'}
        ,timeout=10)

        if not userinfo_response.ok:
            return redirect(f'{login_url}?error=userinfo_failed')

        user_data = userinfo_response.json()
        email = user_data.get('email')

        if not email:
            return redirect(f'{login_url}?error=no_email')

        print("===BEFORE GET OR CREATE")
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'username':email,
                'first_name': user_data.get('given_name', ''),
                'last_name': user_data.get('family_name', ''),
            },
        )
        print(user_data)
        fullname = f"{user_data.get('given_name')} {user_data.get('family_name')}"
        profile_picture = user_data.get('picture')
        new_user = UserProfile.objects.filter(user=user).update(full_name=fullname,picture_url=profile_picture)



        print("=== AFTER GET OR CREATE ===")

        set_profile = False

        if not user.teams.exists():
            set_profile = True


        refresh = RefreshToken.for_user(user)
        params= urlencode({
            'access': str(refresh.access_token),
            'refresh':str(refresh),
            'set_profile':str(set_profile)
        })
        print(params)
        return redirect(f'{settings.FRONTEND_URL}/auth/success?{params}')

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter

    def get_queryset(self):
        User.objects.filter()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_completed(request):
    updated = UserProfile.objects.filter(user=request.user).update(profile_completed=True)


    return Response({"profile_completed":bool(updated)})















