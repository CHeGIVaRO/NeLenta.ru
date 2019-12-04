import requests, os, re, sys
from bs4 import BeautifulSoup
from datetime import datetime
from multiprocessing.pool import ThreadPool
from multiprocessing import Pool
import time
from transliterate import translit, get_available_language_codes

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
os.environ['DJANGO_SETTINGS_MODULE'] = 'nelenta.settings'
import django
django.setup()
from lenta.models import News, Categori, Rubric
SLEEP_TIME = 15
MAIN_URL = "https://lenta.ru"
session = requests.Session()
headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'
}

def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m): (i + 1) * k + min(i + 1, m)] for i in range(n))


def bd_work(news_title, news_img_path, news_content,  rubric_name, categori_name):
    print(news_title)
    print(rubric_name)
    print(categori_name)
    try:
        News.objects.get(title=news_title)
        print('DUBLICATE!!!!!!!!!!!!!')
    except:
        news = News()
        news.title = news_title
        news.content = news_content
        news.main_image = news_img_path
        try:
            Rubric.objects.get(name=rubric_name)
            print("Rubric TRUE")
        except:
            new_rubric = Rubric()
            new_rubric.name = rubric_name
            new_rubric.save()
            print("Rubric FALSE")
        try:
            Categori.objects.get(name=categori_name)
            print("CATEGORI TRUE")
        except:
            new_categori = Categori()
            new_categori.name = categori_name
            new_categori.rubric = Rubric.objects.get(name=rubric_name)
            new_categori.save()
            print("CATEGORI FALSE")
        news.categori = Categori.objects.get(name=categori_name)
        news.rubric = Rubric.objects.get(name=rubric_name)
        news.shoet_content = news_content[3:35] + "..."
        news.save()
    print("--------------------------------------------------------------------------")


def date_check(soup):
    news_date = soup.find('time', class_='g-date')['datetime']
    news_date = re.match('\d{4}-\d{2}-\d{2}', news_date).group(0)
    news_date = datetime.strptime(news_date, "%Y-%m-%d")
    if news_date.day == datetime.now().day:
        return True
    else:
        return False


def get_content(soup):
    paragraphs = soup.find('div', class_='b-text clearfix js-topic__text').find_all('p')
    content = ''
    for p in paragraphs:
        content += '<p>' + p.text + '</p>' + '<br>'
    return content


def get_fucking_img_url(news_title, soup):
    file_name = translit(news_title, 'ru', reversed=True)
    file_name = file_name.strip().replace(" ", "")
    file_name = ''.join(file_name.split())
    try:
        news_img_url = soup.find('div', class_='b-topic__title-image').find('img')['src']
    except AttributeError:
        news_img_url = ''
    if news_img_url != '':
        file_type = re.search(".[a-z]{3}$", news_img_url)
        file_type = file_type.group(0)
        basedir = os.path.abspath(os.path.dirname(__file__))
        path_file = basedir + "/media/static/images/" + file_name + file_type
        get_pic = requests.get(news_img_url)
        out = open(path_file, "wb")
        out.write(get_pic.content)
        out.close()
        return "static/images/" + file_name + file_type
    return "static/images/blank.jpg"


def get_news_data(rubric_name, categori_name, news_url):
    url = MAIN_URL + news_url
    try:
        html = session.get(url, headers=headers, timeout=20.0)
        soup = BeautifulSoup(html.content, 'lxml')
        if date_check(soup):
            news_title = soup.find('h1', class_='b-topic__title').text
            news_img_path = get_fucking_img_url(news_title, soup)
            news_content = get_content(soup)
            bd_work(news_title, news_img_path, news_content, rubric_name, categori_name)
    except:
        print(url)
        print("Я пропустил")


def get_news_url(rubric_name, categori_name, categori_url):
    url = MAIN_URL + categori_url
    try:
        html = session.get(url, headers=headers, timeout=20.0)
    except:
        time.sleep(SLEEP_TIME)
        html = session.get(url, headers=headers, timeout=20.0)
    soup = BeautifulSoup(html.content, 'lxml')
    news_blocks = soup.find('div', class_='span8').find_all('div', class_='news-list')
    for news_list in news_blocks:
        news_elements = news_list.find_all('div', class_='news')
        for news in news_elements:
            news_url = news.find('a')['href']
            get_news_data(rubric_name, categori_name, news_url)


def get_categori(rubric_name, rubric_url):
    print(rubric_url)
    print(rubric_name)
    for id, rubric in enumerate(rubric_url):
        url = MAIN_URL + rubric
        try:
            html = session.get(url, headers=headers, timeout=20.0)
        except:
            time.sleep(SLEEP_TIME)
            html = session.get(url, headers=headers, timeout=20.0)
        soup = BeautifulSoup(html.content, 'lxml')
        sub_menu = soup.find_all('a', class_='item dark')
        for str in sub_menu:
            categori_name = str.text
            categori_url = str['href']
            get_news_url(rubric_name[id], categori_name, categori_url)


def get_rubric():
    rubric_name_list = []
    rubric_url_list = []
    try:
        html = session.get(MAIN_URL, headers=headers, timeout=20.0)
    except:
        time.sleep(SLEEP_TIME)
        html = session.get(MAIN_URL, headers=headers, timeout=20.0)
    soup = BeautifulSoup(html.content, 'lxml')
    main_menu = soup.find_all('li', class_='b-sidebar-menu__list-item')
    for str in main_menu:
        rubric_name = str.find('a').text
        rubric_url = str.find('a')['href']
        if rubric_name != 'Главное':
            rubric_name_list.append(rubric_name)
            rubric_url_list.append(rubric_url)
            # get_categori(rubric_name, rubric_url)
    pool = Pool(4)
    rubric_url_list = list(split(rubric_url_list, 4))
    rubric_name_list = list(split(rubric_name_list, 4))
    pool.starmap(get_categori, zip(rubric_name_list, rubric_url_list))

if __name__ == "__main__":
    start_time = time.time()
    get_rubric()
    print(time.time() - start_time)
