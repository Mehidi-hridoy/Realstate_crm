from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=254, blank=True)
    members=models.ManyToManyField(User, related_name='teams')
    created_by=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__ (self):
        return self.name

