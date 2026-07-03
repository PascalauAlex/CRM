from collections import Counter

from django.db.models import Count, Sum, Value, Q
from django.db.models.functions import Concat
from django.shortcuts import  redirect
from django.utils.http import urlencode
from rest_framework.decorators import api_view
from rest_framework.permissions import  AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
import requests

from client.models import Client
from crm_backend import settings
from tasks.models import Tasks
from team.models import Team
from userprofile.serializer import GoogleAuthSerializer
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from core.models import GoogleCalendarCredential
from lead.models import Lead




class GoogleCalendarAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        serializer = GoogleAuthSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data.get('code')
        error = serializer.validated_data.get('error')

        frontend_redirect_url = f'{settings.FRONTEND_URL}/calendar'

        if error or not code:
            params = urlencode({'error': error or 'no_code'})
            return redirect(f'{frontend_redirect_url}?{params}')

        # 1. Schimbă codul pe token-uri
        token_response = requests.post(
            'https://oauth2.googleapis.com/token',
            data={
                'code': code,
                'client_id': settings.GOOGLE_OAUTH_CLIENT_ID,
                'client_secret': settings.GOOGLE_OAUTH_CLIENT_SECRET,
                'redirect_uri': f'{settings.BACKEND_URL}/api/v1/google/calendar/auth/',
                'grant_type': 'authorization_code',
            },
            timeout=10,
        )
        if not token_response.ok:
            return redirect(f'{frontend_redirect_url}?error=token_exchange_failed')

        tokens = token_response.json()
        access_token = tokens.get('access_token')
        refresh_token = tokens.get('refresh_token')
        expires_in = tokens.get('expires_in')
        scope = tokens.get('scope', '')

        # 2. Identifica userul dupa email (callback-ul nu are JWT)
        userinfo = requests.get(
            'https://www.googleapis.com/oauth2/v3/userinfo',
            headers={'Authorization': f'Bearer {access_token}'},
            timeout=10,
        )
        if not userinfo.ok:
            return redirect(f'{frontend_redirect_url}?error=userinfo_failed')

        email = userinfo.json().get('email')
        if not email:
            return redirect(f'{frontend_redirect_url}?error=no_email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return redirect(f'{frontend_redirect_url}?error=user_not_found')

        # 3. Salveaza credențialul
        expiry = None
        if expires_in:
            expiry = timezone.now() + datetime.timedelta(seconds=int(expires_in))

        credential, _ = GoogleCalendarCredential.objects.get_or_create(user=user)
        if refresh_token:
            credential.refresh_token = refresh_token
        credential.scopes = scope.split() if scope else None
        credential.expiry = expiry
        credential.save()

        return redirect(f'{frontend_redirect_url}?status=success')

@api_view(['GET'])
def dashboard_statistics(request):
    # Data extraction
    team = Team.objects.filter(members__in= [request.user]).first()
    lead_statuses_count = Lead.objects.filter(team=team).values('status').annotate(count=Count('id'))
    lead_assigned_to_ids = Lead.objects.filter(team=team) \
        .exclude(assigned_to__isnull=True) \
        .values_list('assigned_to', flat=True)
    lead_statuses_count = Lead.objects.filter(team=team).values('status').annotate(count=Count('id'))


    assigned_members = list(lead_assigned_to_ids)
    if assigned_members:
        most_frequent = Counter(assigned_members).most_common(1)[0][0]

    cutoff = timezone.now() - datetime.timedelta(days=14)
    stale_leads = (Lead.objects.filter(team=team)
                   .exclude(status__in=['won', 'lost', 'inactive'])
                   .filter(Q(last_contacted_date__lt=cutoff) | Q(last_contacted_date__isnull=True))
                   .count())
        


    client_statuses_count = Client.objects.filter(team=team).values('status').annotate(count=Count('id'))
    team_members = User.objects.filter(teams=team)
    task_statuses_count = Tasks.objects.filter(team=team).values('status').annotate(count=Count('id'))



    #Leads
    lead_status_map = {row['status']: row['count'] for row in lead_statuses_count}

    total_leads =  sum(lead_status_map.values())
    won_leads = lead_status_map.get('won',0)
    lost_leads = lead_status_map.get('lost',0)
    closed = won_leads + lost_leads
    conversion_rate = (won_leads / closed) *100 if closed else 0
    lead_sources_count = (Lead.objects
                          .filter(team=team)
                          .exclude(source__isnull=True)
                          .exclude(source__exact='')
                          .values('source')
                          .annotate(count=Count('id'))
                          .order_by('-count'))

    lead_value_by_stage = (Lead.objects
                           .filter(team=team)
                           .values('status')
                           .annotate(total=Sum('estimated_value'))
                           .order_by('-total'))

    lead_count_by_member = (Lead.objects
                            .filter(team=team)
                            .exclude(assigned_to__isnull=True)
                            .values('assigned_to')
                            .annotate(name=Concat('assigned_to__last_name', Value(' '), 'assigned_to__first_name'),
                                      count=Count('id'))
                            .order_by('-count'))

    lead_stats = {'total_leads':total_leads,
                  'conversion_rate':conversion_rate,
                  'lead_statuses_count':lead_statuses_count,
                  'won_leads':won_leads,
                  'lost_leads':lost_leads,
                  'lead_assigned_to':lead_assigned_to_ids,
                  'lead_sources_count':lead_sources_count,
                  'lead_value_by_stage': lead_value_by_stage,
                  'lead_count_by_member':lead_count_by_member,
                  'stale_leads':stale_leads}

    # Clients
    client_status_map = {row['status']:row['count'] for row in client_statuses_count}
    total_clients = sum(client_status_map.values())

    clients_stats = {'total_clients':total_clients,
                     'client_statuses_count': client_statuses_count,}

    teams_stats = {'total_members':team_members.count()}

    tasks_status_map = {row['status']:row['count'] for row in task_statuses_count}
    tasks_stats = {'total_tasks':sum(tasks_status_map.values())}
    return Response({'lead_stats':lead_stats,'clients_stats':clients_stats,'teams_stats':teams_stats,'tasks_stats':tasks_stats})

