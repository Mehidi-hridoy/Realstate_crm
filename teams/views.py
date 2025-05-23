from django.shortcuts import render, get_object_or_404, redirect
from .models import Team
from .forms import TeamForm  # Fixed typo: 'froom' → 'from' and 'Teamform' → 'TeamForm'
from django.contrib.auth.decorators import login_required
from django .contrib import messages

@login_required
def edit_team(request, pk):
    team = get_object_or_404(Team, created_by=request.user, pk=pk)

    if request.method == 'POST':
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            messages.success(request, 'The changes was saved!')
            return redirect('myaccount')  # Redirect to a detail view or relevant page
        
    else:
        form = TeamForm(instance=team)

    return render(request, 'team/edit_team.html', {
        'form': form,
        'team': team 
    })
  