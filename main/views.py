from django import forms
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ArticleForm, CommentForm
from .models import Article, Comment, Profile
from django.db.models import Q 
from taggit.models import Tag
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
def landing_page(request):
    return render(request, 'landing.html')

@login_required(login_url='login')
def index(request):
    user_object = User.objects.get(username = request.user.username)
    user_profile = Profile.objects.get(user = user_object)
    articles = Article.objects.all()
    tags = Tag.objects.all()
    return render(request, "index.html", {"articles": articles, 'tags':tags, 'user_profile':user_profile})

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == password2:
            if User.objects.filter(email = email).exists():
                messages.info(request, 'Email already sign up')
                return redirect('signup')
            elif User.objects.filter(username = username).exists():
                messages.info(request, 'Username taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                
                #redirect user to profile settings page
                user_login = auth.authenticate(username = username, password = password1)
                auth.login(request, user_login)
                
                #create profile object for new user
                user_model = User.objects.get(username= username)
                new_profile = Profile.objects.create(user = user_model, id_user = user_model.id)
                new_profile.save()
                return redirect('home')
                
        else:
            messages.info(request, 'Passwords do not match')
            return redirect('signup')
        
    return render(request, 'signup.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username = username, password = password)
        
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect(request, login)
            
    return render(request, 'login.html')

@login_required(login_url='login')
def settings(request):
    user_profile = Profile.objects.get(user = request.user)
    if request.method == 'POST':
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            user_profile.profileimg = image
            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            user_profile.profileimg = image
            user_profile.save()
        
        return redirect('settings')
            
    return render(request, 'settings.html', {'user_profile':user_profile})

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('landing_page')

@login_required(login_url='login')
def writepost(request):
    tags = Tag.objects.all()
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=False)
            form.user = request.user
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
    

    