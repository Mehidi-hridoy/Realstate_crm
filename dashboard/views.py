from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from lead.models import Lead
from client.models import Client
from teams.models import Team
from django.db.models import Count


@login_required
def dashboard(request):
    team = Team.objects.filter(created_by=request.user).first()

    recent_leads = Lead.objects.filter(team=team, converted_to_client=False).order_by("-created_at")[:5]
    recent_clients = Client.objects.filter(team=team).order_by("-created_at")[:5]

    # Group and count leads by status and priority for this team only
    status_summary = Lead.objects.filter(team=team,converted_to_client=False).values('status').annotate(total=Count('status'))
    priority_summary = Lead.objects.filter(team=team, converted_to_client=False).values('priority').annotate(total=Count('priority'))

    context = {
        'recent_leads': recent_leads,
        'recent_clients': recent_clients,
        'status_summary': status_summary,
        'priority_summary': priority_summary,
    }

    return render(request, 'dashboard/dashboard.html', context)






def nadira(request):
    return render(request, 'dashboard/nadira.html')