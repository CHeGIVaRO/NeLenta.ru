from django.db import models
from django.conf import settings

class News(models.Model):
    title = models.CharField(max_length = 250, verbose_name = "Заголовок статьи")
    content = models.TextField(verbose_name = "Контент статьи")
    published = models.DateTimeField(auto_now_add = True, db_index = True, verbose_name = "Дата публикации")
    rubric = models.ForeignKey('Rubric', on_delete = models.PROTECT, verbose_name='Рубрика')
    categori = models.ForeignKey('Categori', on_delete = models.PROTECT, verbose_name='Категория')
    watches = models.IntegerField(verbose_name='Просмотры', default=0, editable=False)
    rating = models.IntegerField(verbose_name='Рейтинг', default=0, editable=False)
    shoet_content = models.CharField(verbose_name="раткое описание", max_length=100, default=" ")
    main_image = models.ImageField(upload_to='static/images/', verbose_name="Основное изображение статьи")

    class Meta:
        verbose_name_plural = 'Новости'
        verbose_name = 'Новость'
        ordering =['-published']

class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True, verbose_name = "Название")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Рубрики'
        verbose_name = 'Рубрика'
        ordering =['name']

class Categori(models.Model):
    rubric = models.ForeignKey('Rubric', on_delete = models.PROTECT, verbose_name='Рубрика')
    name = models.CharField(max_length=20, db_index=True, verbose_name = "Название")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'
        ordering =['name']

class Comment(models.Model):
    auth_name = models.CharField(max_length=30, verbose_name="Автор")
    content = models.TextField(verbose_name="Контент коментария")
    rating = models.IntegerField(verbose_name="Рейтинг коментария", editable=False)
    news = models.ForeignKey('News', verbose_name="Новость", on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Коментарии'
        verbose_name = 'Коментарий'
        ordering = ['auth_name']

