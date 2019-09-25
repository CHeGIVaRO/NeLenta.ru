from django.contrib import admin

from .models import News,Rubric,Categori,Comment

class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'published', 'rubric', 'categori', 'watches', 'rating')
    list_display_links = ('title', 'content')

    search_fields = ('title', 'content')
class CommentAdmin(admin.ModelAdmin):
    list_display = ('auth_name', 'content', 'rating', 'news')
    list_display_links = ('content', 'auth_name')

    search_fields = ('auth_name', 'content')

admin.site.register(News, NewsAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Rubric)
admin.site.register(Categori)

# Register your models here.
