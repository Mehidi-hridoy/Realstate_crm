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
    path("<int:pk>/edit/", views.edit_leads, name='edit_leads'),

    path('followups/today/', views.followup_today, name='followup_today'),
    path('followup/next/', views.upcoming_followup, name='upcoming_followup'),
    path('scheduled-followups/', views.scheduled_followup_today, name='scheduled_followups'),
    path('missed-followups/', views.missed_followups, name='missed_followups'),

    
    path('followup/missed/', views.missed_followups, name='followup_missed'),
    path('lead/<int:pk>/', views.lead_details, name='lead_details'),


    
]

