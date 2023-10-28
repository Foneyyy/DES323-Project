from django.shortcuts import render


def index(request):
    context = {
        "title": "Django example",
    }
    return render(request, "index.html", context)


def example_index(request):
    context = {}
    return render(request, "example_w10/index.html", context=context)

