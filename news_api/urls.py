from django.urls import path

from .views import ArticleList



urlpatterns = [
    path('news/', ArticleList.as_view(), name='article-list'),
]
