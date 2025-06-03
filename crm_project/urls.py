from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from crm.views import  about, index
from userprofile.views import signup, myaccount, custom_logout
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('lead.urls',)),  # Fixed 'urls'
    path('', include('dashboard.urls')),
    path('client_list/', include('client.urls')),
    path('myaccount/', myaccount, name='myaccount'),
    path('teams/', include('teams.urls')),  # Fixed 'urls'
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('signup/', signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='userprofile/login.html'), name='login'),
    path('logout/', custom_logout, name='logout'),



]
