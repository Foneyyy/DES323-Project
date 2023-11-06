from datetime import date
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *

# Create your views here.
def data_index_view(request):
    '''This function render index page of Data_sci views'''
    
    return HttpResponse('Welcome to [Your student_id] [Your name] [Your lastname] views!')

def data_sci_item_list_all(request):
    dataset_objs = FootballMatches.objects.all()
    context_data = {
    "filter_type":"All",
    "datasets":dataset_objs
    }
    return render(request, 'data_sci/list_view.html', context= context_data)


def data_sci_item_add(request):
    if request.method == "POST":
        form_data = request.POST
        new_item = FootballMatches(
            home_team = form_data['home_team'],
            away_team = form_data['away_team'],
            home_goals = int(form_data['home_goals']),
            away_goals = int(form_data['away_goals']),
            date = form_data['date'],    
            result = form_data['result'],    
              )
        
        try:
            new_item.save()
        except:
            return HttpResponse("ERROR!" )
        return redirect ('/data_sci/list_item/all' )
    context_data = {
        'item_id' : "New",
        'form_data' :{
            'home_team':"",
            'away_team':"",
            'home_goals':"",
            'away_goals':"",
            'date':"",
            'result':"",
           
            }
    }
    return render(request, 'data_sci/form.html' , context= context_data)

def data_sci_item_edit(request,id):
    try:
        item = FootballMatches.objects.get(id=id)
    except:
        return HttpResponse("ID Not found")
    if request.method == 'POST':
        form_data = request.POST
        item.home_team = form_data['home_team']
        item.away_team = form_data['away_team']
        item.home_goals = form_data['home_goals']
        item.away_goals = form_data['away_goals']
        item.date = date(form_data['date'])
        item.result = form_data['result']
        try:
            item.save()
        except:
            return HttpResponse("ERROR!")
        return redirect('/data_sci/list_item/all')
    context_data = {
        'item_id': id,
        'form_data':{
            'home_team':item.home_team,
            'away_team':item.away_team,
            'home_goals':item.home_goals,
            'away_goals':item.away_goals,
            'date':item.date,
            'result':item.result,
            
        }
    }
    return render(request, 'data_sci/form.html', context= context_data)

def data_sci_item_delete(request, id):
    dataset_objs = FootballMatches.objects.filter(id = id)
    if len(dataset_objs) <= 0:
        return HttpResponse("ID Not found")
    dataset_objs.delete()
    return redirect('/data_sci/list_item/all')