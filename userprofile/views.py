from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from. models import UserProfile
from django.contrib.auth.decorators import login_required
from teams.models import Team
from django.contrib.auth import logout

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)  # ✅ Create once
            team = Team.objects.create(name='The Team Name', created_by=user)
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
