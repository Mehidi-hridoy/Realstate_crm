"""from django.utils.timezone import now
from lead.models import Lead
from dashboard.models import FollowUp

def get_followup_today_count(user):
    today = now().date()

    # Get all followups for today by user
    followup_lead_ids = FollowUp.objects.filter(
        user=user,
        followup_date=today
    ).values_list('lead_id', flat=True)

    # Get all leads edited today by the same user
    edited_lead_ids = Lead.objects.filter(
        modified_at__date=today,
        created_by=user
    ).values_list('id', flat=True)

    # Union of both ID lists and count distinct
    all_today_lead_ids = set(followup_lead_ids).union(set(edited_lead_ids))

    return len(all_today_lead_ids)
"""



from django.utils.timezone import now
from lead.models import Lead
from dashboard.models import FollowUp




def get_scheduled_followup_count(user):
    today = now().date()
    if user.is_superuser:
        return Lead.objects.filter(next_followup_date=today).count()
    else:
        return Lead.objects.filter(next_followup_date=today, created_by=user).count()



def get_missed_followup_count(user):
    today = now().date()
    if user is None:
        return 0
    if user.is_superuser:
        # All leads with next_followup_date before today
        return Lead.objects.filter(next_followup_date__lt=today).count()
    else:
        # Only leads created by this user with next_followup_date before today
        return Lead.objects.filter(next_followup_date__lt=today, created_by=user).count()


def get_followup_today_count(user):
    today = now().date()

    if user is None:  # superuser: get all followups and edits today
        followup_lead_ids = FollowUp.objects.filter(
            followup_date=today
        ).values_list('lead_id', flat=True)

        edited_lead_ids = Lead.objects.filter(
            modified_at__date=today
        ).values_list('id', flat=True)

    else:  # regular user: filter by user
        followup_lead_ids = FollowUp.objects.filter(
            user=user,
            followup_date=today
        ).values_list('lead_id', flat=True)

        edited_lead_ids = Lead.objects.filter(
            modified_at__date=today,
            created_by=user
        ).values_list('id', flat=True)

    all_today_lead_ids = set(followup_lead_ids).union(set(edited_lead_ids))

    return len(all_today_lead_ids)

    # If you want to return the actual leads instead of count, uncomment below:
    # return Lead.objects.filter(id__in=all_today_lead_ids)
