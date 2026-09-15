from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .filters import TaskFilter
from .models import Tasks , TaskAutomationRule
from tasks.serializers import TaskSerializers , TaskAutomationRuleSerializer
from .services import trigger_automation_rules
from team.models import Team
from lead.models import Lead


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializers
    permission_classes = [IsAuthenticated, ]
    filterset_class = TaskFilter
    filter_backends = [DjangoFilterBackend]


    def get_queryset(self):
        # User can acces only the tasks in his team
        print(self.request.user)
        team = Team.objects.filter(members__in=[self.request.user]).first()
        status = self.request.query_params.get('status')

        queryset = Tasks.objects.filter(team=team).select_related(
            'lead', 'assigned_to'
        ).order_by('due_date')

        if status:
            queryset = queryset.filter(status=status)
        else:
            queryset = queryset.filter(status__in=['open','inprogress'])

        return queryset



        return Tasks.objects.filter(team=team).select_related(
            'lead', 'assigned_to'
        ).order_by('due_date')

    def perform_create(self, serializer):
        team = Team.objects.filter(members__in=[self.request.user]).first()
        assigned_to = self.request.data.get('assigned_to')
        lead_id = self.request.data.get('lead_id')
        invalid_status = ['won','lost']
        if assigned_to:
            from django.contrib.auth.models import User
            assigned_user = User.objects.get(id=assigned_to)
        else:
            assigned_user = self.request.user
        if lead_id:
            lead=Lead.objects.get(pk=lead_id)
            if lead.status in invalid_status:
                return Response({'error':"Current lead status is in invalid statuses"},status=400)

        else:
           return Response({"error":'Lead id is needed to create the task'},status=400)


        serializer.save(
            team=team,
            assigned_to=assigned_user,
            lead=lead

        )
        return Response({'Success':'Task created succesfully'},status=200)


class TaskAutomationRuleViewSet(viewsets.ModelViewSet):
    serializer_class = TaskAutomationRuleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        team = Team.objects.filter(members__in=[self.request.user]).first()
        return TaskAutomationRule.objects.filter(team=team)

    def perform_create(self, serializer):
        team = Team.objects.filter(members__in=[self.request.user]).first()
        serializer.save(team=team)



class LeadTaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        lead_id = self.kwargs['pk']
        team = Team.objects.filter(members__in=[self.request.user]).first()
        lead = Lead.objects.filter(id__in=[lead_id]).first()

        return Tasks.objects.filter(team=team,lead=lead).select_related(
            'lead'
        )

    def perform_create(self, serializer):
        team = Team.objects.filter(members__in=[self.request.user]).first()
        serializer.save(
            team=team,
            assigned_to=self.request.user,
        )


































