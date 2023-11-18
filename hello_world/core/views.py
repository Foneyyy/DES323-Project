from django.shortcuts import redirect, render
from django.http import JsonResponse, HttpResponse
import json
import os


from sklearn.model_selection import train_test_split
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.preprocessing import LabelEncoder

import pandas as pd
from data_sci.models import FootballMatches

def index(request):
    context = {
    }
    return render(request, "index.html", context)

def teams(request):
    context = {
    }
    return render(request, "teams.html", context)

def prediction(request):
    teams = [
        {"value":"Arsenal", "name": "Arsenal"}, 
        {"value":"Aston Villa", "name": "Aston Villa"}, 
        {"value":"Bournemouth", "name": "Bournemouth"}, 
        {"value":"Brentford", "name": "Brentford"}, 
        {"value":"Brighton", "name": "Brighton & Hove Albion"}, 
        {"value":"Burnley", "name": "Burnley"}, 
        {"value":"Chelsea", "name": "Chelsea"}, 
        {"value":"Crystal Palace", "name": "Crystal Palace"}, 
        {"value":"Everton", "name": "Everton"}, 
        {"value":"Fulham", "name": "Fulham"}, 
        {"value":"Liverpool", "name": "Liverpool"}, 
        {"value":"Luton Town", "name": "Luton Town"}, 
        {"value":"Manchester City", "name": "Manchester City"}, 
        {"value":"Manchester Utd", "name": "Manchester United"}, 
        {"value":"Newcastle Utd", "name": "Newcastle United"}, 
        {"value":"Nott'ham Forest", "name": "Nottingham Forest"}, 
        {"value":"Sheffield Utd", "name": "Sheffield United"}, 
        {"value":"Tottenham", "name": "Tottenham Hotspur"}, 
        {"value":"West Ham", "name": "West Ham United"}, 
        {"value":"Wolves", "name": "Wolverhampton Wanderers"}, 
    
    ]

    codespace_name = os.getenv("CODESPACE_NAME")
    codespace_domain = os.getenv("GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN")
    codespace_url = f'https://{codespace_name}-8000.{codespace_domain}'

    context = {
        'teams': teams,
        'url': codespace_url
    }

    return render(request, "prediction.html", context)

def about(request):
    context = {
    }
    return render(request, "about.html", context)


def import_data_csv(request):
    csv_url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQFnpIL9V4VCSdMSw4pnC2atxHyc0rNZl4RJ2XourJ6e3-wEfD5cT6JVW3PeuNUTTFvngEK0fm9CyYX/pub?output=csv'
    df = pd.read_csv(csv_url)
    data_sets = df[["Home","HomeGoals","AwayGoals","Away","Date","FTR"]]
    sucesss = []
    errors = []
    for index, row in data_sets.iterrows():
        instance = FootballMatches(
            home_team = row['Home'],
            away_team = row['Away'],
            home_goals = int(row['HomeGoals']),
            away_goals = int(row['AwayGoals']),
            date = row['Date'],
            result = row['FTR'],
        )
        try:
            instance.save()
            sucesss.append(index)
        except:
            errors.append(index)
    return JsonResponse({"success_indexs":sucesss, "error_indexs": errors})

def train_model():
    matches = FootballMatches.objects.all().values()
    df = pd.DataFrame(matches)

    label_encoders = {}
    features = ['home_team', 'away_team']
    
    for feature in features:
        le = LabelEncoder()
        df[feature] = le.fit_transform(df[feature])
        label_encoders[feature] = le

    df = df.drop(columns=['date', 'id','home_goals','away_goals'])
    X = df.drop(columns=['result'])
    y = df['result']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

    etc = ExtraTreesClassifier(n_estimators=100, random_state=42)
    etc.fit(X_train, y_train)

    return etc, label_encoders
    

def model(request):
    if request.method == 'POST':
        try:
            new_match_data = json.loads(request.body)
            new_match = {
                'home_team': new_match_data['home_team'],
                'away_team': new_match_data['away_team'],
            }
        except:
            return JsonResponse({'error': 'Invalid JSON data'})

        etc, label_encoders = train_model()
        features = ['home_team', 'away_team']

        for feature in features:
            new_match[feature] = label_encoders[feature].transform([new_match[feature]])[0]

        new_match_df = pd.DataFrame([new_match])

        pred = etc.predict_proba(new_match_df)

        outcome_prob = []
        for x in pred[0]:
            rounded_prob = round(x, 2)
            outcome_prob.append(rounded_prob)

        response_data = {
            'home_lose': outcome_prob[0],
            'draw': outcome_prob[1],
            'home_win': outcome_prob[2],
        }

        return JsonResponse(response_data)
    else:
        return HttpResponse({'error': 'Invalid request method'})
