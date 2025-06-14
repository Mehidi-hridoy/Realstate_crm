from .models import Lead, LeadChangeLog 
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from .forms import AddLeadForm  
from .models import Lead
from django.contrib import messages
from client.models import Client
from teams.models import Team
from django.db.models import Count
from datetime import datetime,date
from django.utils.timezone import now
from collections import defaultdict
from django.utils.timezone import localtime
from django.urls import reverse
from django.utils.http import urlencode
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
import pandas as pd
from django.http import HttpResponse
from io import BytesIO


from django.contrib.auth.models import User
@login_required
def leads_list(request):
    leads = Lead.objects.all()
    users=User.objects.all()
    total_leads = leads.count()
    users = User.objects.all()  # Pass this to the template

    return render(request, 'lead/leads_list.html', {
        'leads': leads,
        'total_leads': total_leads,
        'users': users,
    })



@login_required
@user_passes_test(lambda u: u.is_superuser)  # Only allow superusers to transfer leads
def lead_transfer_view(request):
    if request.method == 'POST':
        lead_ids = request.POST.getlist('lead_ids')
        new_owner_id = request.POST.get('new_owner')

        if not lead_ids or not new_owner_id:
            messages.warning(request, "Please select at least one lead and a new owner.")
            return redirect('lead:leads_list')

        try:
            new_owner = User.objects.get(id=new_owner_id)
        except User.DoesNotExist:
            messages.error(request, "Selected user does not exist.")
            return redirect('lead:leads_list')

        leads_updated = Lead.objects.filter(id__in=lead_ids).update(created_by=new_owner)
        messages.success(request, f"✅ Successfully {leads_updated} leads transferred from {new_owner} to user: {new_owner.username}.")
        return redirect('lead:leads_list')

    return redirect('lead:leads_list')




@login_required 
def lead_download_excel(request):
    leads = Lead.objects.all()
    df = pd.DataFrame(list(leads))

    # Create a BytesIO buffer
    buffer = BytesIO()

    # Write Excel to the buffer
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Leads')

    # Seek to the beginning of the stream
    buffer.seek(0)

    # Create response with correct headers
    response = HttpResponse(
        buffer,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=All_Leads.xlsx'

    return response






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

    return redirect('lead:leads_list')




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
def lead_followup_and_history(request, pk):
    lead = get_object_or_404(Lead, id=pk)

    referer = request.META.get('HTTP_REFERER')
    default_redirect = reverse('followup_today')
    redirect_to = (
        request.GET.get('redirect_to') or
        request.POST.get('redirect_to') or
        referer or
        default_redirect
    )

    lead_status_choices = Lead.LEAD_STAGE_CHOICES
    followup_methods = Lead.FOLLOWUP_STATUS_CHOICES
    project_type_choices = Lead.PROJECT_CHOICES

    if request.method == "POST":
        new_status = request.POST.get('lead_status')
        new_description = request.POST.get('description', '').strip()
        new_followup_date_str = request.POST.get('next_followup_date')
        new_project_type = request.POST.get('project_type')
        new_followup_method = request.POST.get('followup_method')

        if not new_followup_date_str:
            messages.error(request, "Next Follow-up Date is required.")
            query = urlencode({'redirect_to': redirect_to})
            return redirect(f"{request.path}?{query}")

        changes = []

        # Lead Status Change
        if new_status and lead.lead_status != new_status:
            changes.append(('lead_status', lead.lead_status, new_status))
            lead.lead_status = new_status

        # Clear next follow-up if lead is marked sold
        if new_status and new_status.lower() == "sold_onboard":
            changes.append(('next_followup_date', str(lead.next_followup_date), 'None'))
            lead.next_followup_date = None

        # Description
        if lead.description != new_description:
            changes.append(('description', lead.description, new_description))
            lead.description = new_description

        # Project Type
        current_project_type = getattr(lead, 'projecttype', '')
        if new_project_type and current_project_type != new_project_type:
            changes.append(('projecttype', current_project_type, new_project_type))
            setattr(lead, 'projecttype', new_project_type)

        # Follow-up Method
        current_method = getattr(lead, 'next_followup_by', '')
        if new_followup_method and current_method != new_followup_method:
            changes.append(('next_followup_by', current_method, new_followup_method))
            setattr(lead, 'next_followup_by', new_followup_method)

        # Next Follow-up Date
        try:
            new_followup_date = datetime.strptime(new_followup_date_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            messages.error(request, "Invalid format for Next Follow-up Date.")
            query = urlencode({'redirect_to': redirect_to})
            return redirect(f"{request.path}?{query}")

        if new_followup_date.date() < date.today():
            messages.error(request, "Next Follow-up Date cannot be in the past.")
            query = urlencode({'redirect_to': redirect_to})
            return redirect(f"{request.path}?{query}")

        if lead.next_followup_date != new_followup_date and new_status.lower() != "sold on-board":
            changes.append(('next_followup_date', str(lead.next_followup_date), str(new_followup_date)))
            lead.next_followup_date = new_followup_date

        if changes:
            lead.modified_at = now()
            lead.save()

            for field, old, new_val in changes:
                LeadChangeLog.objects.create(
                    lead=lead,
                    changed_by=request.user,
                    field_name=field,
                    old_value=old or '',
                    new_value=new_val or ''
                )
            messages.success(request, "Lead updated successfully.")

        return redirect(redirect_to)

    # GET Request — Prepare Change Logs
    logs = LeadChangeLog.objects.filter(lead=lead).order_by('change_date')

    grouped_logs = defaultdict(list)
    for log in logs:
        dt = localtime(log.change_date).strftime('%Y-%m-%d %H:%M')
        grouped_logs[dt].append(log)

    grouped_data = []
    last_stage = lead.lead_status or "(blank)"

    for dt, logs_group in sorted(grouped_logs.items()):
        lead_status_old = None
        lead_status_new = None
        next_followup_date = None

        for log in logs_group:
            field = log.field_name.lower()
            if field == 'lead_status':
                lead_status_old = log.old_value or last_stage
                lead_status_new = log.new_value or last_stage
            elif field == 'next_followup_date':
                next_followup_date = log.new_value

        grouped_data.append({
            'datetime': dt,
            'logs': logs_group,
            'next_followup_date': next_followup_date,
            'lead_status_old': lead_status_old or last_stage,
            'lead_status_new': lead_status_new or last_stage,
        })

        if lead_status_new and lead_status_new != "(blank)":
            last_stage = lead_status_new

    grouped_data.reverse()

    return render(request, 'lead/lead_followup_and_history.html', {
        'lead': lead,
        'lead_status_choices': lead_status_choices,
        'followup_methods': followup_methods,
        'project_type_choices': project_type_choices,
        'description': lead.description or '',
        'project_status': getattr(lead, 'projecttype', ''),
        'last_comment': getattr(lead, 'last_comment', ''),
        'followup_method': getattr(lead, 'next_followup_by', ''),
        'grouped_data': grouped_data,
        'redirect_to': redirect_to,
    })





