from django.db import models
from django.contrib.auth.models import User
from teams.models import Team

class Client(models.Model):
    
    name=models.CharField(max_length=50)
    team=models.ForeignKey(Team, related_name='clients', on_delete=models.CASCADE)
    email=models.EmailField()
    description=models.TextField(blank=True, null=True)
    created_by=models.ForeignKey(User, related_name='clients', on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)  # ✅ tuple


    def __str__ (self):
        return self.name