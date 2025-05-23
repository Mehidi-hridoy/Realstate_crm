from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import AddLeadForm  
from .models import Lead
from django.contrib import messages
from client.models import Client
from teams.models import Team

@login_required
def leads_list(request):
    leads=Lead.objects.filter(created_by=request.user,converted_to_client=False)
    return render( request, 'lead/leads_list.html',{
        'leads':leads
    })
    
@login_required
def leads_details(request,pk):
    lead=get_object_or_404(Lead, created_by=request.user,pk=pk)

    return render(request,'lead/leads_details.html',{
        'lead':lead
    })


@login_required
def add_lead(request):
    team=Team.objects.filter(created_by=request.user).first()
    if request.method == 'POST':
        form = AddLeadForm(request.POST)
        if form.is_valid():
            
            team=Team.objects.filter(created_by=request.user).first()
            lead = form.save(commit=False)
            lead.created_by = request.user
            lead.team=team
            lead.save()
            messages.success(request, 'The lead has created successfully.')
            return redirect('dashboard')
    else:
        form = AddLeadForm()
        
    return render(request, 'lead/add_lead.html', {
        'form': form,
        'team':team,
    })


@login_required
def leads_delete(request,pk):
    lead=get_object_or_404(Lead, created_by=request.user,pk=pk)
    lead.delete()
    messages.success(request, 'The lead was deleted.')

    return redirect('leads_list')


@login_required
def edit_leads(request, pk):
    lead = get_object_or_404(Lead, created_by=request.user, pk=pk)

    if request.method == "POST":
        form = AddLeadForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            messages.success(request, 'The changes were saved.')
            return redirect('leads_list')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = AddLeadForm(instance=lead)   

    return render(request, 'lead/edit_lead.html', {
        'form': form,
        'lead': lead,
    })


@login_required
def convert_to_client(request, pk):
    lead = get_object_or_404(Lead, created_by=request.user, pk=pk)  # Capital "L" in Lead
    team=Team.objects.filter(created_by=request.user)[0]

    # Create a new client using lead's data
    client = Client.objects.create(
        name=lead.name,
        email=lead.email,
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
