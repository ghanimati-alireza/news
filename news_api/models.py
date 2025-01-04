from django.db import models

class Article(models.Model):
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=1000)
    description = models.TextField()
    url = models.URLField()
    url_to_image = models.URLField()
    published_date = models.DateTimeField()
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

