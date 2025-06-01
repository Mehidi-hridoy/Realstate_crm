from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Client
from django.contrib import messages
from .forms import AddClientForm
from teams.models import Team
@login_required
def client_list(request):
    clients=Client.objects.filter(created_by=request.user)
    return render(request,'client/clients_list.html', {
        'clients': clients
    })
@login_required
def clients_detail(request, pk):  
    client= get_object_or_404(Client, created_by=request.user, pk=pk)
    return render (request,'client/clients_detail.html',{
        'client': client
    })

@login_required
def add_client(request):
    if request.method == 'POST':
        form = AddClientForm(request.POST)
        if form.is_valid():
            team=Team.objects.filter(created_by=request.user)[0]
            client = form.save(commit=False)
            client.created_by = request.user
            client.team=team
            client.save()
            messages.success(request, 'The client has created successfully.')
            return redirect('dashboard')
    else:
        form = AddClientForm()
        
    return render(request, 'client/add_clients.html', {
        'form': form
    })




@login_required
def client_delete(request,pk):
    client=get_object_or_404(Client, created_by=request.user,pk=pk)
    client.delete()
    messages.success(request, 'The client was deleted.')

    return redirect('client_list')


@login_required
def edit_clients(request, pk):
    client = get_object_or_404(Client, created_by=request.user, pk=pk)

    if request.method == "POST":
        form = AddClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, 'The changes were saved.')
            return redirect('client_list')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = AddClientForm(instance=client)   

    return render(request, 'client/client_edit.html', {
        'form': form,
        'client': client,
    })
