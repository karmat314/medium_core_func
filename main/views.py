from django import forms
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ArticleForm, CommentForm
from .models import Article, Comment
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
    comments = Comment.objects.filter(article = article)
    form = CommentForm()
    tags = Tag.objects.all()
    if request.method == 'POST':
        # get the article by article_id
        # A comment form
        form = CommentForm(request.POST)
        if form.is_valid():
            # Create a Comment object before saving it to the database
            comment = form.save(commit=False)
            # Assign the article to the comment
            comment.article = article
            # Save the comment to the database
            comment.save()
        else:
            form = CommentForm()
    comments = Comment.objects.filter(article = article)
    
    return render(request, 'article_detail.html', {'article':article, 'form':form, 'tags':tags, 'comments':comments})

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
    
""" def commentOnArticle(request, article_id):
    if request.method == 'POST':
        # get the article by article_id
        article = get_object_or_404(Article, id = article_id)
        comment = None
        comments = None
        # A comment form
        form = CommentForm(data=request.POST)
        if form.is_valid():
            # Create a Comment object before saving it to the database
            comment = form.save(commit=False)
            # Assign the article to the comment
            comment.article = article
            # Save the comment to the database
            comment.save()
            comments = Comment.objects.filter(article = article)
        else:
            comments = Comment.objects.filter(article = article)
            form = CommentForm()
    return render(request, 'article_detail.html', {'article': article, 'form': form, 'comments': comments}) """
    