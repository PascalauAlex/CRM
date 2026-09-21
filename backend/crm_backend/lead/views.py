import csv
from datetime import timedelta
from django.db.models.functions import Concat
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404, ListAPIView
from django.db.models import F
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
import openpyxl
from openpyxl.styles import Font
from django.utils import timezone
from tasks.services import trigger_automation_rules
from .serializers import LeadSerializer , LeadNoteSerializer, LostReasonSerializer
from .models import Lead , LeadNote, LostReason
from team.models import Team, User
from rest_framework.pagination import PageNumberPagination
from lead.filters import LeadFilter
from rest_framework.decorators import action
from django.db.models import Value
from rest_framework.response import Response
from lead.services import convert_lead_to_client
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer


def get_team(member_id):
    team = Team.objects.filter(members__in=[member_id]).first()
    return team



class LeadPagination(PageNumberPagination):
    page_size = 10

    def paginate_queryset(
        self, queryset, request, view = ...
    ):
        if 'page' not in request.query_params:
            return None

        return super().paginate_queryset(queryset, request, view)

class LeadViewSet(viewsets.ModelViewSet):
    serializer_class = LeadSerializer
    queryset = Lead.objects.all()
    pagination_class = LeadPagination

    #Filters
    filterset_class = LeadFilter
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        team = Team.objects.filter(members__in= [self.request.user]).first()

        one_week = timezone.now() - timedelta(days=7)

        Lead.objects.filter(
            team=team,
            modified_at__lt=one_week
        ).exclude(
            status__in=['won','lost','inactive']
        ).update(previous_status=F('status'),
            status='inactive',priority='high')

        """select_related -> without Django makes an query to get assigned_to, team, created_by -> N+1
           for each lead LeadSerializer was looking to serialize assigned_to using UserSerializer
           in this was we prefetch userprofile making the query faster
        """
        return self.queryset.filter(team=team).select_related(
            'assigned_to__userprofile', # FK -> User (accesed in serializer)
            'team',        # FK -> Team
            'created_by__userprofile',  # FK -> User
        ).prefetch_related('product_interests')


    def perform_update(self, serializer):
        obj = self.get_object()
        old_status = obj.status
        lost_reason = self.request.data.get('lost_reason_id')
        lost_moment = None

        member_id = self.request.data.get('assigned_to')
        new_checklist = self.request.data.get('checklist')

        if obj.status == 'won' or obj.status == 'lost':
            raise ValidationError({'error':'The current lead cannot be modified!'})

        new_status = obj.status
        calculated_confidence = obj.confidence
        new_priority = obj.priority

        if new_checklist is not None:
            calculated_confidence = 5
            is_contacted = new_checklist.get('new',{}).get('contacted',False)
            is_had_budget = new_checklist.get('contacted',{}).get('has_budget',False)
            can_solve_problem = new_checklist.get('contacted',{}).get('can_solve_problem',False)
            is_decision_maker = new_checklist.get('contacted',{}).get('is_decision_maker',False)
            offer_send = new_checklist.get('inprogress',{}).get('offer_send',False)
            offer_discussed = new_checklist.get('inprogress',{}).get('offer_discussed',False)
            negotiation_started = new_checklist.get('inprogress',{}).get('negotiation_started',False)
            won = new_checklist.get('won',{}).get('won',False)
            lost = new_checklist.get('lost',{}).get('lost',False)

            if is_contacted:
                calculated_confidence +=10

                if obj.status == 'new':
                    new_status = 'contacted'

            if is_had_budget : calculated_confidence += 10
            if can_solve_problem : calculated_confidence += 10
            if is_decision_maker : calculated_confidence += 15

            if(is_had_budget or can_solve_problem or is_decision_maker) and obj.status == 'contacted':
                new_status = 'inprogress'

            if offer_send: calculated_confidence += 15
            if offer_discussed: calculated_confidence += 10
            if negotiation_started: calculated_confidence += 15

            if calculated_confidence > 100:
                calculated_confidence = 100

            match calculated_confidence:
                case val if val < 25:
                    new_priority = 'low'
                case val if val < 70:
                    new_priority = "medium"
                case _:
                    new_priority = 'high'

            if lost:
                new_status = 'lost'
                new_priority = 'low'
            if won:
                new_status = 'won'


            if lost_reason:
                lost_moment = timezone.now()



        print(lost_moment)
        if member_id:
            user = User.objects.get(pk=member_id)
            serializer.save(assigned_to=user, status= new_status, confidence = calculated_confidence , priority = new_priority, lost_at= lost_moment)
        else:
            serializer.save(status = new_status, confidence = calculated_confidence, priority = new_priority, lost_at= lost_moment)

        if new_status != old_status:
            updated_lead = serializer.instance
            trigger_automation_rules(updated_lead,new_status)
        if new_status == 'won' and old_status != 'won':
            convert_lead_to_client(lead=serializer.instance)




    def perform_create(self, serializer):
        team = Team.objects.filter(members__in=[self.request.user]).first()
        initial_confidence = 5
        priority = 'low'
        serializer.save(team = team,created_by=self.request.user,confidence = initial_confidence , priority=priority)





    @action(detail=False, methods=['get'], url_path='exportCSV')
    def export_csv(self,request):
        team = get_team(request.user)

        """ annotate() adds a calculated column to every row of the queryset """
        queryset = Lead.objects.filter(team=team).annotate(
            assigned_to_name = Concat('assigned_to__last_name', Value(' '), 'assigned_to__first_name')
        ).values(
            'id','company','contact_person','email','phone','estimated_value','status',
            'priority','assigned_to_name','created_at'
        )
        fieldnames = ['id','company','contact_person','email',
                      'phone','estimated_value','status',
                      'priority','assigned_to_name','created_at']
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="leads.csv"'
        response['Access-Control-Expose-Headers'] = 'Content-Disposition'

        writer = csv.DictWriter(response,fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(queryset)

        won_leads = Lead.objects.filter(status='won')
        total = 0
        total = sum(won.estimated_value for won in won_leads)


        writer.writerow({field: '' for field in fieldnames})
        writer.writerow({
            'id': 'Total leads:',
            'company': queryset.count(),
            **{field: '' for field in fieldnames[2:]}
        })
        writer.writerow({field: '' for field in fieldnames})
        writer.writerow({
            'id': 'Leads won',
        })
        writer.writerow({
            'id':'Total value:',
            'company': total
        })

        return response

    @action(detail=False, methods=['get'], url_path='exportXLSX')
    def export_xlsx(self, request):
        team = get_team(request.user)


        queryset = Lead.objects.filter(team=team).annotate(
            assigned_to_name=Concat('assigned_to__last_name', Value(' '), 'assigned_to__first_name')
        ).values(
            'id', 'company', 'contact_person', 'email', 'phone', 'estimated_value',
            'status', 'priority', 'assigned_to_name', 'created_at'
        )

        fieldnames = ['id', 'company', 'contact_person', 'email',
                      'phone', 'estimated_value', 'status',
                      'priority', 'assigned_to_name', 'created_at']


        workbook = openpyxl.Workbook()
        worksheet = workbook.active
        worksheet.title = 'Leads'


        worksheet.append(fieldnames)
        for cell in worksheet[1]:
            cell.font = Font(bold=True)


        for lead in queryset:
            row = []
            for field in fieldnames:
                value = lead[field]

                if field == 'created_at' and value is not None:
                    value = timezone.localtime(value).replace(tzinfo=None)
                row.append(value)
            worksheet.append(row)


        won_leads = Lead.objects.filter(status='won')
        total = sum(won.estimated_value for won in won_leads)

        worksheet.append([])  # rand gol
        worksheet.append(['Total leads:', queryset.count()])
        worksheet.append([])  # rand gol
        worksheet.append(['Leads won'])
        worksheet.append(['Total value:', total])


        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="leads.xlsx"'
        response['Access-Control-Expose-Headers'] = 'Content-Disposition'

        workbook.save(response)  # response e file-like
        return response

    @action(detail=False, methods=['get'], url_path='exportPDF')
    def export_pdf(self, request):
        team = Team.objects.filter(members__in=[request.user]).first()

        # acelasi queryset ca la CSV/XLSX
        queryset = Lead.objects.filter(team=team).annotate(
            assigned_to_name=Concat('assigned_to__last_name', Value(' '), 'assigned_to__first_name')
        ).values(
            'id', 'company', 'contact_person', 'email', 'phone', 'estimated_value',
            'status', 'priority', 'assigned_to_name', 'created_at'
        )

        fieldnames = ['id', 'company', 'contact_person', 'email',
                      'phone', 'estimated_value', 'status',
                      'priority', 'assigned_to_name', 'created_at']

        # 1. raspunsul + documentul (A4 pe orizontala, ca sa incapa 10 coloane)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="leads.pdf"'
        response['Access-Control-Expose-Headers'] = 'Content-Disposition'

        doc = SimpleDocTemplate(
            response,
            pagesize=landscape(A4),
            leftMargin=1 * cm, rightMargin=1 * cm,
            topMargin=1 * cm, bottomMargin=1 * cm,
        )

        # 2. stiluri pentru text (necesare ca textul lung sa se rupa pe randuri)
        styles = getSampleStyleSheet()
        cell_style = ParagraphStyle('cell', parent=styles['Normal'], fontSize=7, leading=9)
        header_style = ParagraphStyle('header', parent=cell_style,
                                      textColor=colors.white, fontName='Helvetica-Bold')

        # 3. datele tabelului: primul rand = antet, apoi cate un rand per lead
        table_data = [[Paragraph(name, header_style) for name in fieldnames]]
        for lead in queryset:
            row = []
            for field in fieldnames:
                value = lead[field]
                if field == 'created_at' and value is not None:
                    value = timezone.localtime(value).strftime('%Y-%m-%d %H:%M')
                text = '' if value is None else str(value)  # None -> celula goala
                row.append(Paragraph(text, cell_style))
            table_data.append(row)

        # 4. latime fixa pe coloane (suma ~26 cm < 27.7 cm utili in A4 landscape)
        col_widths = [1 * cm, 3.5 * cm, 3 * cm, 4 * cm, 2.5 * cm, 2.5 * cm, 2 * cm, 2 * cm, 3 * cm, 2.7 * cm]

        table = Table(table_data, colWidths=col_widths, repeatRows=1)  # repeatRows=1 -> antet pe fiecare pagina
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),  # antet albastru
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f3f4f6')]),  # randuri zebra
        ]))

        # 5. sumarul (tabel mic separat) - filtram pe team, ca la fix-ul de data trecuta
        won_leads = Lead.objects.filter(team=team, status='won')
        total = sum(won.estimated_value for won in won_leads)

        summary_style = ParagraphStyle('summary', parent=styles['Normal'], fontSize=9)
        summary_data = [
            [Paragraph('Total leads:', summary_style), Paragraph(str(queryset.count()), summary_style)],
            [Paragraph('Leads won:', summary_style), Paragraph(str(won_leads.count()), summary_style)],
            [Paragraph('Total value:', summary_style), Paragraph(str(total), summary_style)],
        ]
        summary_table = Table(summary_data, colWidths=[4 * cm, 4 * cm])
        summary_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f3f4f6')),
        ]))

        # 6. asamblam documentul dintr-o lista de "flowables" si il construim
        elements = [
            Paragraph('Leads export', styles['Title']),
            Spacer(1, 0.4 * cm),
            table,
            Spacer(1, 0.6 * cm),
            summary_table,
        ]
        doc.build(elements)  # doc.build scrie direct in response (e file-like)

        return response






    # Function defined for agregating all leads to perform analysis based on all leads.
    # No pagination included , returns all the leads of the curent team
    @action(detail=False, methods=['get'], url_path='fetchAllLeads')
    def fetch_all_leads(self,request):
        team = Team.objects.filter(members__in= [self.request.user]).first()
        if not team:
            return Response({'error':'Team was not found, create your team or join a team to fetch all the leads!'})
        queryset = Lead.objects.filter(team=team).select_related('assigned_to__userprofile','team','assigned_to').prefetch_related('product_interests')
        serialized_data = LeadSerializer(queryset,many=True).data

        response = Response(serialized_data,content_type='application/json')

        return response



class LeadNoteViewSet(viewsets.ModelViewSet):
    serializer_class = LeadNoteSerializer
    queryset = LeadNote.objects.all()
    pagination_class = None
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        team = Team.objects.filter(members__in= [self.request.user]).first()
        lead_id = self.request.query_params.get('lead_id')

        return self.queryset.filter(team=team).filter(lead_id = lead_id)

    def perform_create(self, serializer):
        team = Team.objects.filter(members__in = [self.request.user]).first()
        lead_id = self.request.data.get('lead_id')

        lead = get_object_or_404(Lead, id = lead_id , team = team)

        serializer.save(team=team , created_by = self.request.user , lead = lead)


class LostReasonViewSet(viewsets.ModelViewSet):
    queryset = LostReason.objects.all()
    serializer_class = LostReasonSerializer
    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]























