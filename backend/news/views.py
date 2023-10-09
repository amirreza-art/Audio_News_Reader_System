from rest_framework import generics
from .models import News
from .serializers import NewsByCategorySerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import Http404

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
    