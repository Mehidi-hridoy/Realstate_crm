from django.urls import path

from.import views

urlpatterns=[
    path('dashboard', views.dashboard, name='dashboard'),
    path('nadinum', views.nadira, name='nadira' ),
    path('leads/high-priority/', views.high_priority_leads, name='high_priority_leads'),
    path('leads/prospect/', views.prospect_leads, name='prospect_leads'),
    path('leads/junk/', views.junk_leads, name='junk_leads'),
    path('leads/lead/', views.lead_leads, name='lead_leads'),
    path('leads/lost/', views.lost_leads, name='lost_leads'),
    path('leads/sold-onboard/', views.sold_leads, name='sold_onboard_leads'),
    path('leads/hold/', views.hold_leads, name='hold_leads'),
    path('lead/<int:lead_id>/add_followup/', views.add_followup, name='add_followup'),
    path('followups/today/', views.followup_today, name='followup_today'),
    path('followup/next/', views.followup_next, name='followup_next'),
    path("<int:pk>/edit/", views.edit_leads, name='edit_leads'),
    
]

