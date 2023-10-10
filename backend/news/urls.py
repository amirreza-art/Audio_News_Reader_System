from django.urls import path
from .views import NewsByCategoryView, NewsDetailView

urlpatterns = [
    path('category/news/<int:category_id>/', NewsByCategoryView.as_view(), name='newsByCategoryID_list'),
    path('category/news/<str:category_title>/', NewsByCategoryView.as_view(), name='newsByCategoryTitle_list'),
    path('the-news/<int:guid>/', NewsDetailView.as_view(), name='NewsByGuid_detail'),
]
