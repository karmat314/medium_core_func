from django import forms
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import ArticleForm
from .models import Article
from django.db.models import Q 
from taggit.models import Tag
# Create your views here.
def index(request):
    articles = Article.objects.all()
    tags = Tag.objects.all()
    return render(request, "index.html", {"articles": articles, 'tags':tags})

def writepost(request):
    tags = Tag.objects.all()
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=True)
            return redirect('home')
        return render(request, 'writepost.html', {'form': form, 'tags':tags})
    
    else:
        form = ArticleForm()

    return render(request, 'writepost.html', {'form': form, 'tags':tags})

def articleDetail(request, id):
    article = Article.objects.get(id = id)
    tags = Tag.objects.all()
    return render(request, 'article_detail.html', {'article':article, 'tags':tags})

def searchArticle(request):
     # Query all posts
    tags = Tag.objects.all()
    search_article = request.GET.get('search')
    if search_article:
        articles = Article.objects.filter(Q(title__icontains=search_article))
    else:
        # If not searched, return default posts
        articles = Article.objects.all().order_by("-created_on")
    return render(request, 'index.html', {'articles': articles, 'tags':tags})

    
def articlesByTag(request):
    tag = request.GET.get("tag")
    tags = Tag.objects.all()
    if (tag):
        articles = Article.objects.filter(tags__name__in=[tag]) #tags filtered by tag parameter
        return render(request, 'index.html', {'articles': articles, 'tags':tags})
    else:
        articles = Article.objects.all()
        return render(request, 'index.html', {'articles': articles, 'tags':tags})
    