import select
from django.db.models import Model
from mailjet_rest.client import ValidationError
from rest_framework import viewsets
from rest_framework.decorators import permission_classes
from urllib3 import Retry

from products import serializer
from products.models import Product, ProductCategory, LeadProductInterest
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView

from products.serializer import ProductSerializer, ProductCategorySerializer, LeadProductSerializer
from team.models import Team
from lead.models import Lead


# Create your views here.



class ProductsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get_queryset(self):
        team = Team.objects.filter(members__in=[self.request.user]).first()
        return self.queryset.filter(team=team)



    def perform_create(self, serializer):
        team = Team.objects.filter(members__in= [self.request.user]).first()
        if not team:
            raise ValidationError({
                'team':'You must be assigned to a team to create products.'
            })
        serializer.save(
            team=team
        )



class ProductCategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,IsAdminUser]
    serializer_class = ProductCategorySerializer
    queryset = ProductCategory.objects.all()


    def get_queryset(self):
        team = Team.objects.filter(members__in= [self.request.user]).first()
        return self.queryset.filter(team=team)

class ProductLeadViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = LeadProductSerializer
    queryset = LeadProductInterest.objects.all()

    def get_queryset(self):
        qs = LeadProductInterest.objects.all()
        lead_id = self.request.query_params.get('lead')
        if lead_id is not None:
            qs = qs.filter(lead_id=lead_id)
        return qs








