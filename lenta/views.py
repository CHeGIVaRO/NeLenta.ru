from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Rubric, Categori, News
import json
from django.http import HttpResponse

def pagination(list_news, numb_page):
    p = Paginator(list_news, 12)
    return p.page(numb_page).object_list

def get_content(request):
    number_page = request.GET.get('number_page')
    newses = pagination(News.objects.all(), number_page)
    context = {"newses": newses}
    return render(request, 'ajax_content.html', context)

def test_pagination(request, number_page):
    p = Paginator(News.objects.all(), 12)
    pages_num = p.num_pages
    string_for_test = ""
    print("-----------------------------------------------------")
    print(number_page)
    for news in p.page(number_page).object_list:
        print(news.title)
        string_for_test += news.title
    print(string_for_test)
    print("-----------------------------------------------------")
    context = {"string_for_test": string_for_test,
               "pages_num": pages_num}
    dump = json.dumps(context)
    return HttpResponse(dump, content_type='application/json')


def index(request):
    rubrics = Rubric.objects.all()
    categories = Categori.objects.all()
    newses = News.objects.all()
    #newses = pagination(News.objects.all(), 1)
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

def news_page(request, news_id):
    news = News.objects.get(pk=news_id)
    categories = Categori.objects.all()
    rubrics = Rubric.objects.all()
    context = {"rubrics": rubrics,
               "categories": categories,
               "news": news
               }
    return render(request, 'news_page.html', context)

