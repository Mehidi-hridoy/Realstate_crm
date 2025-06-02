from .models import Lead, LeadChangeLog 
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import AddLeadForm  
from .models import Lead
from django.contrib import messages
from client.models import Client
from teams.models import Team
from django.db.models import Count
from datetime import datetime
from django.utils.timezone import now
from collections import defaultdict
from django.utils.timezone import localtime




@login_required
def leads_list(request):
    if request.user.is_superuser:
        leads = Lead.objects.filter(converted_to_client=False)
    else:
        leads = Lead.objects.filter(created_by=request.user)

    return render(request, 'lead/leads_list.html', {
        'leads': leads,
        'total_leads': leads.count(),
    })






"""def leads_list(request):
    if request.user.is_superuser:
        leads=Lead.objects.filter(created_by=request.user,converted_to_client=False)
    else:
        leads = Lead.objects.filter(created_by=request.user)
    return render( request, 'lead/leads_list.html',{
        'leads':leads
    })
    
"""

@login_required
def add_lead(request):
    team = Team.objects.filter(created_by=request.user).first()
    if request.method == 'POST':
        form = AddLeadForm(request.POST)
        if form.is_valid():
            lead = form.save(commit=False)
            lead.created_by = request.user
            lead.team = team
            lead.save()  # unique_id auto-generated here
            messages.success(request, 'The lead has been created successfully.')
            return redirect('dashboard')
    else:
        form = AddLeadForm()

    return render(request, 'lead/add_lead.html', {
        'form': form,
        'team': team,
    })


@login_required
def leads_delete(request, pk):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You do not have permission to delete leads.")

    lead = get_object_or_404(Lead, pk=pk)
    lead.delete()
    messages.success(request, 'The lead was deleted.')

    return redirect('leads_list')


@login_required
def edit_leads(request, pk):
    # Ensure the lead exists and belongs to the logged-in user
    lead = get_object_or_404(Lead, pk=pk, created_by=request.user)

    if request.method == "POST":
        form = AddLeadForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            messages.success(request, "The changes were saved successfully.")
            return redirect("leads_list")
        else:
            messages.error(request, "Please correct the error(s) below.")
    else:
        form = AddLeadForm(instance=lead)

    context = {
        "form": form,
        "lead": lead,
    }

    return render(request, "lead/edit_lead.html", context)

@login_required
def convert_to_client(request, pk):
    lead = get_object_or_404(Lead, created_by=request.user, pk=pk)  # Capital "L" in Lead
    team=Team.objects.filter(created_by=request.user)[0]
    
    client = Client.objects.create(
        name=lead.name,
        email=lead.primaryemail,
        description=lead.description,  # Typo fixed: 'descripton' -> 'description'
        created_by=request.user,
        team=team,
    )
    # Mark the lead as converted
    lead.converted_to_client = True
    lead.save()

    # Show success message and redirect
    messages.success(request, "The lead has been converted to a client.")
    return redirect('leads_list')








@login_required
def update_followup(request, pk):
    lead = get_object_or_404(Lead, id=pk)

    lead_status_choices = Lead.LEAD_STAGE_CHOICES
    followup_methods = Lead.FOLLOWUP_STATUS_CHOICES
    project_type_choices = Lead.PROJECT_CHOICES

    if request.method == "POST":
        new_status = request.POST.get('lead_status')
        new_description = request.POST.get('description', '')
        new_followup_date_str = request.POST.get('next_followup_date')
        new_project_type = request.POST.get('project_type')
        new_followup_method = request.POST.get('followup_method', '')

        changes = []

        # Lead Status
        if new_status and lead.lead_status != new_status:
            changes.append(('lead_status', lead.lead_status, new_status))
            lead.lead_status = new_status

        # Description
        if lead.description != new_description:
            changes.append(('description', lead.description, new_description))
            lead.description = new_description or ''

        # Next Follow-up Date
        if new_followup_date_str:
            try:
                new_followup_date = datetime.strptime(new_followup_date_str, '%Y-%m-%d').date()
                if lead.next_followup_date != new_followup_date:
                    changes.append(('next_followup_date', lead.next_followup_date, new_followup_date))
                    lead.next_followup_date = new_followup_date
            except ValueError:
                pass

        # Project Type
        if new_project_type and getattr(lead, 'projecttype', None) != new_project_type:
            changes.append(('projecttype', lead.projecttype, new_project_type))
            lead.projecttype = new_project_type

        # Follow-up Method
        if hasattr(lead, 'next_followup_by') and lead.next_followup_by != new_followup_method:
            changes.append(('next_followup_by', lead.next_followup_by, new_followup_method))
            lead.next_followup_by = new_followup_method or ''

        # Save changes and log
        if changes:
            lead.modified_at = now()
            lead.save()

            for field, old, new in changes:
                LeadChangeLog.objects.create(
                    lead=lead,
                    changed_by=request.user,
                    field_name=field,
                    old_value=str(old or ''),
                    new_value=str(new or '')
                )

        return redirect('lead:leads_list')

    # GET method: render form
    return render(request, 'lead/update_followup.html', {
        'lead': lead,
        'lead_status_choices': lead_status_choices,
        'followup_methods': followup_methods,
        'project_type_choices': project_type_choices,
        'description': lead.description or '',
        'project_status': getattr(lead, 'projecttype', ''),  # FIXED: Match model field
        'last_comment': getattr(lead, 'last_comment', ''),
        'followup_method': getattr(lead, 'next_followup_by', ''),
    })








@login_required
def lead_change_history(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    logs = LeadChangeLog.objects.filter(lead=lead).order_by('change_date')

    grouped_logs = defaultdict(list)
    for log in logs:
        dt = localtime(log.change_date).strftime('%Y-%m-%d %H:%M')  # group by minute
        grouped_logs[dt].append(log)

    last_stage = lead.lead_status or "(blank)"  # Default to lead's initial stage
    grouped_data = []

    for dt, logs_group in sorted(grouped_logs.items()):
        lead_status_old = None
        lead_status_new = None
        next_followup_date = None

        for log in logs_group:
            if log.field_name.lower() == 'lead_status':
                lead_status_old = log.old_value or last_stage or "(blank)"
                lead_status_new = log.new_value or last_stage or "(blank)"
            if log.field_name.lower() == 'next_followup_date':
                next_followup_date = log.new_value

        # If no stage info was found in this group, use the last known stage
        if lead_status_old is None and lead_status_new is None:
            lead_status_old = last_stage or "(blank)"
            lead_status_new = last_stage or "(blank)"

        grouped_data.append({
            'datetime': dt,
            'logs': logs_group,
            'next_followup_date': next_followup_date,
            'lead_status_old': lead_status_old,
            'lead_status_new': lead_status_new,
        })

        # Update last_stage after appending to use in next iteration
        if lead_status_new and lead_status_new != "(blank)":
            last_stage = lead_status_new

    grouped_data = list(reversed(grouped_data))

    return render(request, 'lead/lead_change_history.html', {
        'lead': lead,
        'grouped_data': grouped_data,
    })









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
    return render(request, 'lead/leads_details.html', context)
