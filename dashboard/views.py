from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from lead.models import Lead
from client.models import Client
from teams.models import Team
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from dashboard.models import FollowUp
from django.utils.timezone import now
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db.models import Q, F
from lead.utils import get_followup_today_count  # adjust import path as needed

@login_required
def dashboard(request):
    if request.user.is_superuser:
        lead_filter = {}
        client_filter = {}
    else:
        team = Team.objects.filter(created_by=request.user).first()
        lead_filter = {'team': team, 'created_by': request.user}
        client_filter = {'team': team, 'created_by': request.user}

    total_leads = Lead.objects.filter(**lead_filter).count()
    sold_count = Lead.objects.filter(**lead_filter, lead_status='sold_onboard').count()
    hold_count = Lead.objects.filter(**lead_filter, lead_status='hold').count()
    lead_count = Lead.objects.filter(**lead_filter, lead_status='lead').count()
    junk_count = Lead.objects.filter(**lead_filter, lead_status='junk').count()
    prospect_count = Lead.objects.filter(**lead_filter, lead_status='prospect').count()
    high_prospect_count = Lead.objects.filter(**lead_filter, lead_status='high_prospect').count()
    lost_count = Lead.objects.filter(**lead_filter, lead_status='lost').count()

    leads_by_status = (
        Lead.objects.filter(**lead_filter)
        .values('lead_status')
        .annotate(count=Count('id'))
    )

    recent_leads = Lead.objects.filter(**lead_filter).order_by("-created_at")[:5]
    recent_clients = Client.objects.filter(**client_filter).order_by("-created_at")[:5]

    if request.user.is_superuser:
        followup_today_count = get_followup_today_count(None)  # Adjust inside function to handle None
    else:
        followup_today_count = get_followup_today_count(request.user)

    context = {
        'total_leads': total_leads,
        'followup_today_count': followup_today_count,
        'sold_count': sold_count,
        'lead_count': lead_count,
        'hold_count': hold_count,
        'junk_count': junk_count,
        'prospect_count': prospect_count,
        'high_prospect_count': high_prospect_count,
        'lost_count': lost_count,
        'recent_leads': recent_leads,
        'recent_clients': recent_clients,
        'leads_by_status': leads_by_status,
    }

    return render(request, 'dashboard/dashboard.html', context)


@login_required
def add_followup(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)

    # You can customize how notes or followup date come in from a form:
    notes = request.POST.get('notes', '')

    FollowUp.objects.create(
        lead=lead,
        user=request.user,
        followup_date=now().date(),
        notes=notes,
    )
    return redirect('dashboard')  # or redirect to a lead detail page

@login_required
def followup_today(request):
    today = now().date()

    if request.user.is_superuser:
        # Superuser sees all follow-ups and all leads edited today
        followups = FollowUp.objects.filter(followup_date=today).select_related('lead')
        leads_edited_today = Lead.objects.filter(modified_at__date=today)
    else:
        # Regular users see only their own follow-ups and leads they created and edited today
        followups = FollowUp.objects.filter(user=request.user, followup_date=today).select_related('lead')
        leads_edited_today = Lead.objects.filter(
            modified_at__date=today,
            created_by=request.user
        )
    # Collect unique leads from both follow-up and edited sets
    leads_from_followup = {f.lead for f in followups}
    all_today_leads = leads_from_followup.union(set(leads_edited_today))

    # Build a structured list for display
    leads_data = []
    for lead in all_today_leads:
        leads_data.append({
            'lead': lead,
            'is_followed': lead in leads_from_followup,
            'is_edited': lead.modified_at.date() == today,
        })
    today_created_count = sum(1 for item in leads_data if item['lead'].created_at.date() == today)


    context = {
        'leads_data': leads_data,
        'today': today,
        'today_created_count': today_created_count,
    }
    return render(request, 'dashboard/followup_today.html', context)


@login_required
def followup_next(request):
    today = timezone.now().date()

    next_followups = FollowUp.objects.filter(
        user=request.user,
        followup_date__gt=today
    ).filter(
        Q(lead__modified_at__gt=F('modified_at')) | Q(followup_date__gt=today)
    ).order_by('followup_date').select_related('lead')

    context = {
        'next_followups': next_followups,
        'page_title': "Next Follow-ups",
    }
    return render(request, 'dashboard/followup_next.html', context)




@login_required
def high_priority_leads(request):
    if request.user.is_superuser:
        # Admin can see all high priority leads
        leads = Lead.objects.filter( lead_status='high_prospect')
    else:
        # Normal user can only see their own team's leads created by them
        team = Team.objects.filter(created_by=request.user).first()
        leads = Lead.objects.filter(
            team=team,
            created_by=request.user,
             
            lead_status='high_prospect')  # use actual stored value here
        
    total_high_priority_leads = leads.count()
    return render(request, 'dashboard/high_priority_leads.html', {
        'leads': leads,
        'total_high_priority_leads': total_high_priority_leads,})


@login_required
def prospect_leads(request):
    if request.user.is_superuser:
        # Admin can see all prospect leads
        leads = Lead.objects.filter( lead_status='prospect')
    else:
        # Normal user can only see their own team's leads created by them
        team = Team.objects.filter(created_by=request.user).first()
        leads = Lead.objects.filter(
            team=team,
            created_by=request.user,
            
            lead_status='prospect'
        )
    total_prospect_leads = leads.count()

    return render(request, 'dashboard/prospect_leads.html', {
        'leads': leads,
        'total_prospect_leads': total_prospect_leads,
    })

"""@login_required
def prospect_leads(request):
    team = Team.objects.filter(created_by=request.user).first()
    if request.user.is_superuser:
        leads = Lead.objects.filter(team=team,  lead_status='prospect')
    else:
        leads = Lead.objects.filter(team=team, created_by=request.user,  lead_status='prospect')
    total_prospect_leads = leads.count()
    

    return render(request, 'dashboard/prospect_leads.html', {
        'leads': leads,
        'total_prospect_leads': total_prospect_leads,
        
        })
"""
@login_required
def junk_leads(request):
    # Check if the user is a superuser
    if request.user.is_superuser:
        # Admin can see all junk leads
        leads = Lead.objects.filter( lead_status='junk')
    else:
        # Normal user can only see their own team's leads created by them
        team = Team.objects.filter(created_by=request.user).first()
        leads = Lead.objects.filter(
            team=team, 
            
            lead_status='junk')
    total_junk_leads = leads.count()  # This line is not used, so it can be removed

    return render(request, 'dashboard/junk_leads.html', {
        'leads': leads,
        'total_junk_leads': total_junk_leads,})

@login_required
def lead_leads(request):
    if request.user.is_superuser:
        # Admin can see all leads
        leads = Lead.objects.filter( lead_status='lead')
    else:
        # Normal user can only see their own team's leads created by them
        team = Team.objects.filter(created_by=request.user).first()
        leads=Lead.objects.filter(
            team=team,
            
            lead_status='lead')
    tolal_leads = leads.count()
    #leads = Lead.objects.filter(team=team, lead_status='lead') if team else []

    return render(request, 'dashboard/lead_leads.html', {
        'leads': leads,
        'tolal_leads': tolal_leads,})

@login_required
def lost_leads(request):
    # Check if the user is a superuser
    if request.user.is_superuser:
        # Admin can see all lost leads
        leads = Lead.objects.filter( lead_status='lost')
    else:
            # Normal user can only see their own team's leads created by them
        team = Team.objects.filter(created_by=request.user).first()
        leads = Lead.objects.filter(
        team=team,
         
        lead_status='lost') 
    total_lost_leads = leads.count()
    return render(request, 'dashboard/lost_leads.html', {
        'leads': leads,
        'total_lost_leads': total_lost_leads,
    })


@login_required
def sold_leads(request):
    # Check if the user is a superuser
    if request.user.is_superuser:
        # Admin can see all sold leads
        leads = Lead.objects.filter( lead_status='sold_onboard')
    else:
            # Normal user can only see their own team's leads created by them
        team = Team.objects.filter(created_by=request.user).first()
        leads = Lead.objects.filter(
            team=team, 
            
            lead_status='sold_onboard') 
    total_sold_leads = leads.count()

    return render(request, 'dashboard/sold_leads.html', {
        'leads': leads,
        'total_sold_leads': total_sold_leads,
    })


@login_required
def hold_leads(request):
    # Check if the user is a superuser
    if request.user.is_superuser:
        # Admin can see all hold leads
        leads = Lead.objects.filter( lead_status='hold')
    else:
            # Normal user can only see their own team's leads created by them
        team = Team.objects.filter(created_by=request.user).first()
        leads = Lead.objects.filter(team=team,  lead_status='hold') 
    total_hold_leads = leads.count()

    return render(request, 'dashboard/hold_leads.html', {
        'leads': leads,
        'total_hold_leads': total_hold_leads,})



@login_required
def nadira(request):
    return render(request, 'dashboard/nadira.html')

