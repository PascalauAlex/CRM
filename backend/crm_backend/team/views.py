from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.views import APIView


from .serializers import TeamSerializer, UserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Team
from services.generateCode import generate_code

class TeamViewSet(viewsets.ModelViewSet):
    serializer_class = TeamSerializer
    queryset = Team.objects.all()
    permission_classes = [IsAuthenticated]

    #Overide the get_queryset
    def get_queryset(self):
        return self.queryset.filter(members__in = [self.request.user]).first()

    #The user will be a member of the team
    def perform_create(self, serializer):
        obj = serializer.save(created_by = self.request.user)
        user = self.request.user
        user.is_staff = True
        user.save()
        obj.members.add(self.request.user)
        obj.save()



#Cautam echipele unde userul curent este membru
@api_view(['GET'])
def get_my_team(request):
    team = Team.objects.filter(members__in=[request.user]).prefetch_related('members__userprofile').first()
    serializer = TeamSerializer(team)

    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_invite_code(request):
    team = Team.objects.filter(members__in=[request.user]).prefetch_related('members__userprofile').first()
    if not team:
        return Response({'error':'No team'},status=404)

    generated_code = generate_code()
    team.invite_code = f"{team.name[:3].upper()}-{generated_code}"
    team.save(update_fields=['invite_code'])

    return Response({'invite_code':team.invite_code},status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_team_by_code(request):
    invite_code = request.data.get('invite_code')
    if not invite_code:
        return Response({"error":"No invite code"},status=400)
    user = request.user
    team = Team.objects.filter(invite_code=invite_code).first()

    if not team:
        return Response(
            {'error':'Invalid invite code'},
            status=status.HTTP_404_NOT_FOUND
        )

    if team.members.filter(id=request.user.id).exists():
        return Response(
            {'error':'User is already in this team'},
            status=status.HTTP_400_BAD_REQUEST
        )

    team.members.add(user)

    return Response({"team":team.name,"message":f"User joined team : {team.name}"})



@api_view(['POST'])
def add_member(request):

    username = request.data.get('username')  # email-ul
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')

    try:
        user = User.objects.get(username=username)

        # 2. Actualizăm doar numele și prenumele
        user.first_name = first_name
        user.last_name = last_name
        user.save()


        team = Team.objects.filter(members__in=[request.user]).first()

        if team:
            team.members.add(user)
            return Response({"status": "Success"}, status=201)
        else:
            return Response({"error": "Did not find the team."}, status=404)

    except User.DoesNotExist:
        return Response({"error": "The user was not found."}, status=404)


class UserDetail(APIView):
    def get_object(self,pk):
        try:
            return  User.objects.get(pk = pk)
        except User.DoesNotExist:
            raise Http404

    def get(self,request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)









