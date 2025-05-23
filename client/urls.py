from django.urls import path
from.import views


urlpatterns=[
    path('', views.client_list, name="client_list"),
    path('add_clients/',views.add_client, name='addclient'),
    path('<int:pk>/', views.clients_detail, name='clients_detail'),  
    path('<int:pk>/delete',views.client_delete,name="client_delete"),
    path("<int:pk>/edit", views.edit_clients, name='client_edit'),
    
]