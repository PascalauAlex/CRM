from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.text import slugify
from core.models import Address
from team.models import Team
from datetime import  datetime, timezone



def get_default_checklist():
    return {
        "new": {"contacted": False , "contact_method": None},
        "contacted" : {"has_budget": False, "can_solve_problem":False , "is_decision_maker": False},
        "inprogress": {"offer_send":False , "offer_discussed": False , "negotiation_started": False},
        "lost":{"lost":False,"reason":""},
        "won":{"won":False}
    }



class LostReason(models.Model):
    CATEGORY_CHOICES = [
        ('pricing', 'Pricing & Budget'),
        ('competition', 'Competition'),
        ('product_fit', 'Product Fit'),
        ('timing', 'Timing'),
        ('decision', 'Decision Making'),
        ('engagement', 'Engagement'),
        ('organizational', 'Organizational'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100 , unique=True, blank=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True, help_text='Internal note about when to use this reason')
    is_active = models.BooleanField(default=True, help_text='Uncheck to hide without deleting')
    display_order = models.PositiveIntegerField(default=0, help_text='Lower values show first')

    #Audit
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='created_lost_reasons'
    )


    class Meta:
        ordering = ['category', 'display_order', 'name']
        verbose_name = 'Lost Reason'
        verbose_name_plural = 'Lost Reasons'

    def __str__(self):
        return f"{self.name}"


    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args,**kwargs)

# LLM enum properties

LEAD_STATUSES : list[str] = ['new','contacted','inprogress','lost','won','inactive']
LEAD_PRIORITIES: list[str] = ['low','medium','high']

class Lead(models.Model):
    NEW = 'new'
    CONTACTED = 'contacted'
    INPROGRESS = 'inprogress'
    LOST = 'lost'
    WON = 'won'
    INACTIVE = 'inactive'
    CHOICHES_STATUS = (
        (NEW,'New'),
        (CONTACTED,'Contacted'),
        (INPROGRESS,'In progress'),
        (LOST,'Lost'),
        (WON,'Won'),
        (INACTIVE,'Inactive')
    )
    LOW ='low'
    MEDIUM = 'medium'
    HIGH = 'high'

    CHOICHES_PRIORITY = (
    (LOW,'Low'),
    (MEDIUM,'Medium'),
    (HIGH,'High')
    )
    team = models.ForeignKey(Team,related_name='leads',on_delete=models.CASCADE)
    company = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    email = models.EmailField(db_index=True)
    phone = models.CharField(max_length=20) #TODO: Add django-phonenumber-field
    website = models.CharField(max_length=255, blank=True, null=True)
    confidence = models.IntegerField(blank=True, null=True,validators=[MinValueValidator(0),MaxValueValidator(100)])
    estimated_value = models.DecimalField(max_digits=10,decimal_places=2,blank=True, null=True)
    status = models.CharField(max_length=25,choices=CHOICHES_STATUS,default=NEW)
    previous_status = models.CharField(max_length=25,choices=CHOICHES_STATUS,default=NEW)
    priority = models.CharField(max_length=25, choices=CHOICHES_PRIORITY, default=MEDIUM)
    assigned_to = models.ForeignKey(User,related_name='assignedLeads', blank=True, null=True,on_delete=models.SET_NULL)
    created_by = models.ForeignKey(User,related_name='leads',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    address = models.ForeignKey(Address,on_delete=models.SET_NULL, null=True, blank=True, related_name='leads', help_text='Adress of the lead')
    source = models.CharField(max_length=100, blank=True, null=True)
    next_follow_up_date = models.DateTimeField(blank=True, null=True)
    last_contacted_date = models.DateTimeField(blank=True, null=True)
    lost_reason = models.ForeignKey(
        LostReason,
        on_delete=models.PROTECT, # If the reason is deleted we do not want to delete all the leads with that lost reason
        related_name='leads',
        blank=True,
        null=True
    )
    expected_close_date = models.DateField(blank=True, null=True)
    lost_reason_details = models.TextField(
        blank=True,
        help_text='Additional context about why the lead is lost'
    )
    lost_at = models.DateTimeField(blank=True, null=True)
    checklist = models.JSONField(default=get_default_checklist)

    def __str__(self):
        return f"Lead: {self.company}, status: {self.status}, estimated value {self.estimated_value}"


    @property
    def last_modified(self):
        today = datetime.now(timezone.utc)
        delta = today - self.modified_at # the diference returns timedelta object
        return delta.days #sending the numbers of days as int


    class Meta:
        ordering = ['-created_at']

    def recompute_estimated_value(self):
        total = self.product_interests.aggregate(t=Sum('estimated_value'))['t'] or 0
        Lead.objects.filter(pk=self.pk).update(estimated_value=total)
        self.estimated_value = total
        return total








class LeadNote(models.Model):
    team = models.ForeignKey(Team,related_name='leadNotes',on_delete=models.CASCADE)
    lead = models.ForeignKey(Lead,related_name='leadNotes',on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    body = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='leadNotes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        # Save the note
        super().save(*args, **kwargs)

        fields_to_update = ['modified_at']

        # If the lead was inactive we are setting it to the last status
        if self.lead.status == Lead.INACTIVE:

            self.lead.status = self.lead.previous_status or Lead.INPROGRESS
            fields_to_update.append('status')


        self.lead.save(update_fields=fields_to_update)

    def __str__(self):
        return f"Lead note name: {self.name}, description: {self.body}"

    class Meta:
        ordering = ['-created_at']








