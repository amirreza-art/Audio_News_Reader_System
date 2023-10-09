from django.urls import path
from .views import NewsByCategoryView 

urlpatterns = [
    path('category/news/<int:category_id>/', NewsByCategoryView.as_view(), name='newsByCategory_list'),
]


