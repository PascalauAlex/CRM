from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import SET_NULL
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from lead.models import Lead
from team.models import Team


# Create your models here.


class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self',null=True,blank=True,on_delete=SET_NULL)
    team = models.ForeignKey(Team,null=True,blank=True,on_delete=models.CASCADE)



class Product(models.Model):
    PRODUCT_TYPE = [('product','Product'),('service','Service')]
    UNIT_CHOICES = [('piece', 'Piece'), ('hour', 'Hour'), ('month', 'Month'), ('project', 'Project')]

    sku = models.CharField(max_length=50,unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey(ProductCategory,on_delete=models.PROTECT)
    type = models.CharField(max_length=20,choices=PRODUCT_TYPE)
    unit_of_measure = models.CharField(max_length=20,choices=UNIT_CHOICES)
    base_price = models.DecimalField(max_digits=12,decimal_places=2)
    currency = models.CharField(max_length=3, default='RON')
    vat_rate = models.DecimalField(max_digits=4, decimal_places=2, default=19)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    team = models.ForeignKey(Team,on_delete=models.CASCADE,blank=True,null=True)


class LeadProductInterest(models.Model):
    lead = models.ForeignKey(Lead, related_name='product_interests',on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    discount = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)],blank=True,null=True)
    estimated_value = models.DecimalField(max_digits=12,decimal_places=2,null=True,blank=True)
    notes = models.TextField(blank=True)
    added_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ('lead', 'product')

@receiver(post_save, sender=LeadProductInterest)
@receiver(post_delete, sender=LeadProductInterest)
def _sync_lead_value(sender, instance, **kwargs):
    try:
        lead = instance.lead
    except Lead.DoesNotExist:
        return
    lead.recompute_estimated_value()
