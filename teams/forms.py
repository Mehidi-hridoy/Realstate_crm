from django import forms
from .models import Team

class TeamForm(forms.ModelForm):  # Capital "F" in ModelForm and TeamForm
    class Meta:
        model = Team 
        fields = 'name',  # Include this to specify which fields to use (can be customized)
