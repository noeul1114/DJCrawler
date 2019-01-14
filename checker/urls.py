
from django.urls import path, include

from . import views

urlpatterns = [
    path('unchecked', views.uncheckMain, name='uncheck_main'),
    path('checked', views.checkMain, name='check_main'),
    path('article_checked/<int:article_id>', views.article_checked, name='article_checked'),
    path('article_deleted/<int:article_id>', views.article_deleted, name='article_deleted'),
]
