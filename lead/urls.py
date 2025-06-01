from django.urls import path
from .import views

urlpatterns=[
    path('add-lead/',views.add_lead, name='addlead'),
    path('leads_list', views.leads_list, name="leads_list"),
    path('<int:pk>/delete',views.leads_delete,name="lead_delete"),
    path("<int:pk>/edit", views.edit_leads, name='edit_leads'),
    path("<int:pk>/convert", views.convert_to_client, name="lead_convert"),
    path('lead/<int:pk>/', views.lead_details, name='lead_details')


]