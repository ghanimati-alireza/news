from datetime import datetime

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import NewsFilter
from .models import Article
from .serializers import ArticleSerializer


def save_articles(articles):
    for article in articles:
        if not Article.objects.filter(url=article['url']).exists():
            Article.objects.create(
                author=article.get('author', ''),
                title=article['title'],
                description=article['description'],
                url=article['url'],
                url_to_image=article['urlToImage'],
                published_date=datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ'),
                content=article['content'],
            )

class ArticleList(APIView):
    filter_backends = [DjangoFilterBackend]
    filterset_class = NewsFilter
    def get(self, request):
        queryset = Article.objects.all()
        filterset = self.filterset_class(request.GET, queryset=queryset)
        if filterset.is_valid():
            queryset = filterset.qs
        else:
            return Response(filterset.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = ArticleSerializer(queryset, many=True)
        return Response(serializer.data)


