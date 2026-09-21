from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

from lead.models import Lead
from tasks.services import trigger_automation_rules


@receiver(post_save,sender=Lead)
def automatization_rule(sender,instance,created,**kwargs):
    print("AUTOMATIZATION RULE SIGNAL")
    if created:
        trigger_automation_rules(lead=instance,new_status=instance.status)
