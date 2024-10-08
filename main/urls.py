from django.urls import path
from main.views import*

urlpatterns = [
    path('home/', index, name='home'),
    path('signup/', signup, name='signup'),
    path('', login, name='login'),
    path('logout/', logout, name='logout'),
    path('setting/', settings, name='settings'),
    
    path('write/', writepost, name="write"),
    path('updatearticle/<int:id>/', updatearticle, name="updatearticle"),
    path('deletearticle/<int:id>/', deletearticle, name='deletearticle'),
    
    path('top-articles/', topArticles, name="topArticles"),
    path('newest-articles/', newArticles, name="newArticles"),
    path('article/<int:id>/', articleDetail, name="viewArticle"),
    path('search_results/', searchArticle, name="searchArticle"),
    path('articles_tag/', articlesByTag, name="articlesByTag"),
    path('like-article/', likearticle, name='likearticle')
]
