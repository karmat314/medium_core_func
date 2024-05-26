from django.urls import path
from main.views import*

urlpatterns = [
    path('', index, name='home'),
    path('write/', writepost, name="write"),
    path('article/<int:id>/', articleDetail, name="viewArticle"),
    path('search_results/', searchArticle, name="searchArticle"),
    path('articles_tag/', articlesByTag, name="articlesByTag"),
]
