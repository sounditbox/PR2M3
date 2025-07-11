from django_filters.filters import DateTimeFilter, NumberFilter, BaseInFilter, \
    CharFilter
from django_filters.rest_framework import FilterSet

from posts.models import Article, Comment


class NumberInFilter(BaseInFilter, NumberFilter):
    pass


class ArticleFilter(FilterSet):
    categories = NumberInFilter(field_name='category', lookup_expr='in')
    tags = NumberInFilter(field_name='tags', lookup_expr='in')
    start_date = DateTimeFilter(field_name='created_at', lookup_expr='gte')
    end_date = DateTimeFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Article
        fields = ['tags', 'category']

