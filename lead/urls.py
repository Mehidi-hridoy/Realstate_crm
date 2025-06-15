from django.urls import path
from .import views

app_name = 'lead'

urlpatterns=[
    path('add-lead/', views.add_lead, name='addlead'),
    path('leads_list', views.leads_list, name="leads_list"),
        path('lead_transfer', views.lead_transfer_view, name='lead_transfer'),

    path('<int:pk>/delete',views.leads_delete,name="lead_delete"),
    path("<int:pk>/convert", views.convert_to_client, name="lead_convert"),
    #path('lead/<int:pk>/update/', views.update_followup, name='update_followup'),
    path('lead/<int:pk>/history/', views.lead_followup_and_history, name='lead_change_history'),
    path('leads/download_excel/', views.lead_download_excel, name='lead_download_excel'),

    




]