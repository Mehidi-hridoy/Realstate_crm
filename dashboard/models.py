from django.db import models
from django.contrib.auth.models import User
from lead.models import Lead

class FollowUp(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='followups')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    followup_date = models.DateField(auto_now_add=True)  # date of follow-up
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Follow-up for {self.lead} by {self.user} on {self.followup_date}"
