from django.shortcuts import render

# Create your views here.
from .models import Rubric, Categori, News
def index(request):
    rubrics = Rubric.objects.all()
    categories = Categori.objects.all()
    newses = News.objects.all()
    context = {"rubrics": rubrics,
               "categories": categories,
               "newses": newses
               }
    for categori in categories:
        for rubric in rubrics:
            if rubric.name == categori.rubric.name:
                print(type(categori.rubric))
    return render(request, 'index.html', context)