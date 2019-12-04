from django.shortcuts import render
from .models import Rubric, Categori, News


def index(request):
    rubrics = Rubric.objects.all()
    categories = Categori.objects.all()
    newses = News.objects.all()
    context = {"rubrics": rubrics,
               "categories": categories,
               "newses": newses
               }
    return render(request, 'index.html', context)


def by_rubric(request, rubric_id):
    newses = News.objects.filter(rubric=rubric_id)
    categories = Categori.objects.all()
    rubrics = Rubric.objects.all()
    context = {"rubrics": rubrics,
               "categories": categories,
               "newses": newses
               }
    return render(request, 'by_rubric.html', context)


def by_category(request, categori_id):
    newses = News.objects.filter(categori=categori_id)
    categories = Categori.objects.all()
    rubrics = Rubric.objects.all()
    context = {"rubrics": rubrics,
               "categories": categories,
               "newses": newses
               }
    return render(request, 'by_categori.html', context)

