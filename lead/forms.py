from django import forms
from .models import Lead

class AddLeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        exclude = ['created_by', 'team','unique_id', ]
        widgets = {
            'created_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'phone': forms.TextInput(attrs={
        'type': 'tel',  # numeric keypad on mobile, no spinner buttons
        'maxlength': '11',
        'pattern': r'\d{11}',  # HTML5 pattern for validation (exactly 11 digits)
        'oninput': "this.value = this.value.replace(/[^0-9]/g, '').slice(0,11);"  # JS to allow only digits and limit length
    }),
            'modified_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'next_followup_date': forms.DateInput(attrs={'type': 'date'}),
        }
