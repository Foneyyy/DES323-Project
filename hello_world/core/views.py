from django.shortcuts import render


def index(request):
    context = {
    }
    return render(request, "index.html", context)

def teams(request):
    context = {
    }
    return render(request, "teams.html", context)

def prediction(request):
    context = {
    }
    return render(request, "prediction.html", context)

def about(request):
    context = {
    }
    return render(request, "about.html", context)



def example_index(request):
    context = {}
    return render(request, "example_w10/index.html", context=context)
