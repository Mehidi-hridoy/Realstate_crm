from django import forms
from .models import Lead

class AddLeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        exclude = ['created_by', 'team']
        widgets = {
            'created_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'modified_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'next_followup_date': forms.DateInput(attrs={'type': 'date'}),
        }
