from django_filters import rest_framework as filters
from .models import Article

class NewsFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name="published_date", lookup_expr='gte')
    end_date = filters.DateFilter(field_name="published_date", lookup_expr='lte')
    ordering = filters.OrderingFilter(fields=['published_date'])

    class Meta:
        model = Article
        fields = ['start_date', 'end_date', 'ordering']
