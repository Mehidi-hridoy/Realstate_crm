from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from. models import UserProfile
from django.contrib.auth.decorators import login_required
from teams.models import Team, Plan
from django.contrib.auth import logout


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)

            # Get the default plan (you can adjust this as needed)
            default_plan = get_object_or_404(Plan, name='Free')  # Make sure a "Free" plan exists

            # Create team with the required plan
            team = Team.objects.create(name='teams', created_by=user, plan=default_plan)
            team.members.add(user)
            team.save()

            return redirect('/login/')
    else:
        form = UserCreationForm()

    return render(request, 'userprofile/signup.html', {'form': form})




@login_required
def myaccount(request):
     team = Team.objects.filter(created_by=request.user).first()
     return render(request, 'userprofile/myaccount.html',{
         'team':team
     })


def custom_logout(request):
    logout(request)
    next_url = request.GET.get('next', '/')
    return redirect(next_url)
