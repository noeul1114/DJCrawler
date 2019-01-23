
from django.urls import path, include

from . import views
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('unchecked', views.uncheckMain, name='uncheck_main'),
    path('image_checked/<str:img_name>', views.image_checked, name='image_checked'),

    path('image', views.imageMain, name='image_main'),
    path('checked', views.checkMain, name='check_main'),
    path('article_checked/<int:article_id>', views.article_checked, name='article_checked'),
    path('article_deleted/<int:article_id>', views.article_deleted, name='article_deleted'),

]

if settings.DEBUG:
    urlpatterns += [
        path(r'^C:/Users/willypower/PycharmProjects/DJCrawler/checker/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]