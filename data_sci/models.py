from django.db import models


# Create your models here.

class FootballMatches(models.Model):
    home_team = models.CharField(max_length=255)
    away_team = models.CharField(max_length=255)
    home_goals = models.IntegerField()
    away_goals = models.IntegerField()
    date = models.DateField()
    result = models.CharField(max_length=1)
