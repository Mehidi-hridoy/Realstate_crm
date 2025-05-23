from django.db import models
from django.contrib.auth.models import User



class Plan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    max_leads = models.IntegerField() # type: ignore
    max_clients = models.IntegerField()


    def __str__ (self):
        return self.name


class Team(models.Model):
    name=models.CharField(max_length=100)
    plan=models.ForeignKey(Plan, related_name='teams',on_delete=models.CASCADE)
    members=models.ManyToManyField(User, related_name='teams')
    created_by=models.ForeignKey(User, related_name='created_teams',on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__ (self):
        return self.name

