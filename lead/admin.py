from django.contrib import admin
from .models import Lead
from .forms import AddLeadForm


class LeadAdmin(admin.ModelAdmin):
    form = AddLeadForm   

admin.site.register(Lead, LeadAdmin)
