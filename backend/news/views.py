from rest_framework import generics
from .models import News, Category
from .serializers import NewsByCategorySerializer, NewsSerializer, CategorySerializer
from rest_framework.response import Response
from django.http import Http404
import django_filters


class NewsByCategoryView(generics.ListAPIView):
    serializer_class = NewsByCategorySerializer

    def get_queryset(self):
        if self.kwargs.get('category_id'):
            category_id = self.kwargs['category_id']
            queryset = News.objects.filter(category__id=category_id)

            if not queryset.exists():
                raise Http404()
            
        elif self.kwargs.get('category_title'):
            category_title = self.kwargs['category_title']
            queryset = News.objects.filter(category__title=category_title)

            if not queryset.exists():
                raise Http404() 
            
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)
    

class NewsDetailView(generics.RetrieveAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    lookup_field = "guid"


class CategoryFilter(django_filters.FilterSet):
    last_update = django_filters.DateTimeFilter(field_name='news_items__updated_at__date', lookup_expr="exact")
   
    class Meta:
        model = Category
        fields = ('title', 'last_update')

    @property
    def qs(self):
        queryset = Category.objects.all()
        title = self.request.query_params.get('title')
        if title:
            queryset = queryset.filter(title=title).distinct()

        last_update = self.request.query_params.get('last_update')
        if last_update:
            queryset = queryset.filter(news_items__updated_at__date=last_update).distinct()

        return queryset

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filterset_class = CategoryFilter
