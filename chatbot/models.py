# models.py
from django.db import models
from django.contrib.auth.models import User
import uuid
from django.contrib.postgres.fields import JSONField
from accounts.models import Account

class UserSession(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    current_step = models.CharField(max_length=255, blank=True, null=True)
    state = models.JSONField(default=dict) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    questions_and_answers = models.JSONField(default=dict)  # Store questions and answers

    def __str__(self):
        return f"{self.user.username}"



class Car(models.Model):
    make = models.CharField(max_length=500)
    year = models.PositiveIntegerField()
    model = models.CharField(max_length=500)
    trim = models.CharField(max_length=500)
    color = models.CharField(max_length=500)

    class Meta:
        unique_together = ('make', 'year', 'model', 'trim', 'color')

    def __str__(self):
        return f"{self.year} {self.make} {self.model} {self.trim} {self.color}"

