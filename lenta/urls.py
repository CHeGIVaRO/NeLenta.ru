from django.urls import path
from .views import index, by_rubric, by_category, test_pagination, get_content
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', index, name='index'),
    path('rubric/<int:rubric_id>/', by_rubric, name='by_rubric'),
    path('categori/<int:categori_id>', by_category, name='by_categori'),
    path('testpagination/<int:number_page>', test_pagination, name='test_pagination'),
    path('get_content/', get_content, name='get_content'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)