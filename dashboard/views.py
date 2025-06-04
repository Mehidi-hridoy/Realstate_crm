
from lead.forms import   AddLeadForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from lead.models import Lead
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now # adjust import if needed
from datetime import datetime
from client.models import Client
from teams.models import Team
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from dashboard.models import FollowUp
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db.models import Q, F
from lead.utils import get_followup_today_count,get_missed_followup_count, get_scheduled_followup_count # adjust import path as needed

@login_required
def dashboard(request):
    # Superusers see all leads and clients; others see only their own team's
    if request.user.is_superuser:
        lead_filter = {}
        client_filter = {}
    else:
        team = Team.objects.filter(created_by=request.user).first()
        lead_filter = {'team': team, 'created_by': request.user}
        client_filter = {'team': team, 'created_by': request.user}
        
    # Lead status counts for dashboard metrics
    total_leads = Lead.objects.filter(**lead_filter).count()
    sold_count = Lead.objects.filter(**lead_filter, lead_status='sold_onboard').count()
    hold_count = Lead.objects.filter(**lead_filter, lead_status='hold').count()
    lead_count = Lead.objects.filter(**lead_filter, lead_status='lead').count()
    junk_count = Lead.objects.filter(**lead_filter, lead_status='junk').count()
    prospect_count = Lead.objects.filter(**lead_filter, lead_status='prospect').count()
    high_prospect_count = Lead.objects.filter(**lead_filter, lead_status='high_prospect').count()
    lost_count = Lead.objects.filter(**lead_filter, lead_status='lost').count()

    # Count of leads grouped by their current status
    leads_by_status = (
        Lead.objects.filter(**lead_filter)
        .values('lead_status')
        .annotate(count=Count('id'))
    )

    # Show most recent leads and clients
    recent_leads = Lead.objects.filter(**lead_filter).order_by("-created_at")[:5]
    recent_clients = Client.objects.filter(**client_filter).order_by("-created_at")[:5]

    # Count of today's follow-ups (custom logic based on user access)
    if request.user.is_superuser:
        followup_today_count = get_followup_today_count(None)  # Handle all users in function
    else:
        followup_today_count = get_followup_today_count(request.user)
    today = now().date()
    today_scheduled_count = get_scheduled_followup_count(request.user)



    # Count of upcoming follow-ups after today
    if request.user.is_superuser:
        upcoming_count = Lead.objects.filter(next_followup_date__gt=today).count()
    else:
        upcoming_count = Lead.objects.filter(next_followup_date__gt=today, created_by=request.user).count()



    # Count of follow-ups that were missed (scheduled before today)
    if request.user.is_superuser:
        missed_followup_count = get_missed_followup_count(request.user)
    else:
        missed_followup_count = get_missed_followup_count(request.user)



    # Passing all metrics and data to the dashboard template
    context = {
        'total_leads': total_leads,
        'followup_today_count': followup_today_count,
        'missed_followup_count': missed_followup_count,
        'today_scheduled_count': today_scheduled_count,
        'today': today,
        'upcoming_count': upcoming_count,
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
def lead_details(request, pk):
    if request.user.is_superuser:
        # Superuser can view any lead
        lead = get_object_or_404(Lead, pk=pk)
    else:
        team = Team.objects.filter(created_by=request.user).first()
        lead = get_object_or_404(
            Lead,
            pk=pk,
            team=team,
            created_by=request.user  # Ensures normal users only access their own leads
        )

    # Optional: Group follow-ups by date
    followup_summary = Lead.objects.filter(
        next_followup_date__isnull=False
    ).values('next_followup_date').annotate(
        lead_count=Count('id')
    ).order_by('next_followup_date')

    if request.method == 'POST':
        form = AddLeadForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lead updated successfully.')
            return redirect('lead:leads_list')
    else:
        form = AddLeadForm(instance=lead)

    context = {
        'lead': lead,
        'form': form,
        'followup_summary': followup_summary,
    }
    return render(request, 'dashboard/leads_details.html', context)





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
def missed_followups(request):
    today = now().date()

    if request.user.is_superuser:
        missed_leads = Lead.objects.filter(next_followup_date__lt=today)
    else:
        missed_leads = Lead.objects.filter(next_followup_date__lt=today, created_by=request.user)

    missed_followup_count = get_missed_followup_count(request.user)

    context = {
        'page_title': 'Missed Follow-ups',
        'leads_data': missed_leads,
        'missed_followup_count': missed_followup_count,
        'today': today,
    }
    return render(request, 'dashboard/missed_followups.html', context)



@login_required
def scheduled_followup_today(request):
    today = now().date()

    if request.user.is_superuser:
        leads = Lead.objects.filter(next_followup_date=today)
    else:
        leads = Lead.objects.filter(next_followup_date=today, created_by=request.user)

    today_scheduled_count = get_scheduled_followup_count(request.user)

    return render(request, 'dashboard/scheduled_followup_today.html', {
        'leads': leads,
        'today': today,
        'today_scheduled_count': today_scheduled_count,
    })



@login_required
def upcoming_followup(request):
    today = now().date()

    if request.user.is_superuser:
        # Superuser sees all leads with upcoming follow-ups
        upcoming_leads = Lead.objects.filter(next_followup_date__gt=today)
    else:
        # Regular users see only their own leads with upcoming follow-ups
        upcoming_leads = Lead.objects.filter(
            next_followup_date__gt=today,
            created_by=request.user
        )

    upcoming_count = upcoming_leads.count()

    # Prepare data for display if needed
    leads_data = []
    for lead in upcoming_leads:
        leads_data.append({
            'lead': lead,
            'next_followup_date': lead.next_followup_date,
        })

    context = {
        'leads_data': leads_data,
        'upcoming_count': upcoming_count,
        'page_title': "Upcoming Follow-ups",
    }
    return render(request, 'dashboard/upcoming_followup.html', context)






@login_required
def edit_leads(request, pk):
    lead = get_object_or_404(Lead, pk=pk)

    # Determine where to go after saving: passed in query or post
    redirect_to = request.POST.get('redirect_to') if request.method == "POST" else request.GET.get('redirect_to', 'lead_leads')

    if request.method == "POST":
        form = AddLeadForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            messages.success(request, "The changes were saved successfully.")

            # If it's a URL path (starts with slash), treat as a direct redirect
            if redirect_to.startswith('/'):
                return redirect(redirect_to)
            else:
                # Assume it's a Django view name
                return redirect(redirect_to)
        else:
            messages.error(request, "Please correct the error(s) below.")
    else:
        form = AddLeadForm(instance=lead)
    context = {
        "form": form,
        "lead": lead,
        "redirect_to": redirect_to,
    }

    return render(request, "dashboard/edit_lead.html", context)





@login_required
def lead_leads(request):
    if request.user.is_superuser:
        leads = Lead.objects.filter(lead_status='lead')
    else:
        leads = Lead.objects.filter(created_by=request.user, lead_status='lead')
    total_leads = leads.count()
    return render(request, 'dashboard/lead_leads.html', {
        'leads': leads,
        'total_leads': total_leads,
    })


@login_required
def high_priority_leads(request):
    if request.user.is_superuser:
        leads = Lead.objects.filter( lead_status='high_prospect')
    else:
        leads = Lead.objects.filter( created_by=request.user,  lead_status='high_prospect')  # use actual stored value here
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
        leads = Lead.objects.filter( created_by=request.user,lead_status='prospect'
        )
    total_prospect_leads = leads.count()

    return render(request, 'dashboard/prospect_leads.html', {
        'leads': leads,
        'total_prospect_leads': total_prospect_leads,
    })


@login_required
def junk_leads(request):
    # Check if the user is a superuser
    if request.user.is_superuser:
        # Admin can see all junk leads
        leads = Lead.objects.filter( lead_status='junk')
    else:
        # Normal user can only see their own team's leads created by them
        leads = Lead.objects.filter(created_by=request.user,lead_status='junk')
    total_junk_leads = leads.count()  # This line is not used, so it can be removed

    return render(request, 'dashboard/junk_leads.html', {
        'leads': leads,
        'total_junk_leads': total_junk_leads,})


@login_required
def lost_leads(request):
    # Check if the user is a superuser
    if request.user.is_superuser:
        # Admin can see all lost leads
        leads = Lead.objects.filter( lead_status='lost')
    else:
            # Normal user can only see their own team's leads created by them
        leads = Lead.objects.filter( created_by=request.user, lead_status='lost') 
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
        
        leads = Lead.objects.filter(created_by=request.user, lead_status='sold_onboard') 
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
        leads = Lead.objects.filter(created_by=request.user, lead_status='hold') 
    total_hold_leads = leads.count()

    return render(request, 'dashboard/hold_leads.html', {
        'leads': leads,
        'total_hold_leads': total_hold_leads,})



@login_required
def nadira(request):
    return render(request, 'dashboard/nadira.html')

