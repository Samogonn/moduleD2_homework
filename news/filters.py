from django_filters import FilterSet, DateFilter
from .models import Post

class PostFilter(FilterSet):
    class Meta:
        model = Post

        fields = {
            'datetime': ['gt'],
            'title': ['icontains'],
            'author__author__username': ['icontains'],
        }
