from django.urls import path
from main.views import*

urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('home/', index, name='home'),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('setting/', settings, name='settings'),
    path('write/', writepost, name="write"),
    path('article/<int:id>/', articleDetail, name="viewArticle"),
    path('search_results/', searchArticle, name="searchArticle"),
    path('articles_tag/', articlesByTag, name="articlesByTag"),
]
