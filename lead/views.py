from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import AddLeadForm  
from .models import Lead
from django.contrib import messages
from client.models import Client
from teams.models import Team
from django.db.models import Count



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
def leads_details(request,pk):
    if request.user.is_superuser:
     leads=get_object_or_404(Lead, created_by=request.user,pk=pk)
    else:
        leads = get_object_or_404(Lead, created_by=request.user, pk=pk, converted_to_client=False)

    return render(request,'lead/leads_details.html',{
        'lead':leads
    })


@login_required
def add_lead(request):
    team=Team.objects.filter(created_by=request.user).first()
    if request.method == 'POST':
        form = AddLeadForm(request.POST)
        if form.is_valid():
            lead = form.save(commit=False)
            lead.created_by = request.user  # Automatically assign user
            lead.team = team                # Automatically assign team
            lead.save()
            messages.success(request, 'The lead has been created successfully.')
            return redirect('dashboard')
    else:
        form = AddLeadForm()
        
    return render(request, 'lead/add_lead.html', {
        'form': form,
        'team':team,
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
            return redirect('leads_list')
    else:
        form = AddLeadForm(instance=lead)

    context = {
        'lead': lead,
        'form': form,
        'followup_summary': followup_summary,
    }
    return render(request, 'lead/leads_details.html', context)
