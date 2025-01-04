from django_celery_beat.models import PeriodicTask, IntervalSchedule
from celery import shared_task
from datetime import datetime
import requests
from django.utils.timezone import make_aware
from .models import Article

API_KEY = 'a0076520d94c43e491555d3a4aa9896b'
API_URL = 'https://newsapi.org/v2/top-headlines'


def fetch_articles(page_num):
    """Fetch articles from the API for the given page number."""
    params = {
        'apiKey': API_KEY,
        'country': 'us',
        'pageSize': 2,  # Only fetch 2 articles at a time
        'page': page_num,
    }
    response = requests.get(API_URL, params=params)
    return response.json()


def save_new_articles(articles):
    """Save new articles to the database if not already saved."""
    for article in articles:
        if not Article.objects.filter(url=article['url']).exists():
            Article.objects.create(
                author=article.get('author', ''),
                title=article['title'],
                description=article['description'],
                url=article['url'],
                url_to_image=article['urlToImage'],
                published_date=make_aware(datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')),
                content=article['content'],
            )


@shared_task
def fetch_and_save_news():
    """Fetch and save news articles periodically."""
    last_article = Article.objects.order_by('-published_date').last()
    last_published_date = last_article.published_date or '2025-01-01'

    page_num = 1
    all_articles_new = True

    while all_articles_new:
        data = fetch_articles(page_num)

        if data['status'] == 'ok':
            articles = data['articles']
            new_articles = [article for article in articles if make_aware(
                datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')) > last_published_date]

            if new_articles:

                save_new_articles(new_articles)
                all_articles_new = True
            else:
                all_articles_new = False

        page_num += 1


def schedule_periodic_task():
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=6,
        period=IntervalSchedule.MINUTES,
    )
    PeriodicTask.objects.create(
        interval=schedule,
        name='Fetch and save news periodically',
        task='news_api.tasks.fetch_and_save_news',
    )