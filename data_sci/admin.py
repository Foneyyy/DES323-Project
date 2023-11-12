from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(FootballMatches)
class FootballAdmin(admin.ModelAdmin):
    pass