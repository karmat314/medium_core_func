from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .forms import ArticleForm, CommentForm
from .models import Article, Comment, Profile, LikeArticle
from django.db.models import Q 
from taggit.models import Tag
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

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
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Check if any field is empty
        if not (username and email and password1 and password2):
            messages.error(request, 'All fields are required.')
            return redirect('signup')
        
        if password1 == password2:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email is already in use.')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken.')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                
                user_login = auth.authenticate(username = username, password = password1)
                auth.login(request, user_login)
                
                #create profile object for new user
                user_model = User.objects.get(username= username)
                new_profile = Profile.objects.create(user = user_model, id_user = user_model.id)
                new_profile.save()
                
                return redirect('home')
        else:
            # If passwords don't match, clear the password fields only
            messages.error(request, 'Passwords do not match.')
            # Pass the valid form data back to the signup template
            return render(request, 'signup.html', {'username': username, 'email': email})
    
    # If the request is not POST or if there are any errors, render the signup page with error messages
    return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username:
            messages.info(request, 'Username is required.')
            return redirect('login')
        
        if not password:
            messages.info(request, 'Password is required.')
            return redirect('login')

        user = authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('login')
            
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
    user_object = User.objects.get(username = request.user.username)
    user_profile = Profile.objects.get(user = user_object)
    tags = Tag.objects.all()
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user  # Set the user before saving
            article.save()
            form.save_m2m()
            return redirect('home')  # Redirect to a success page
    else:
        form = ArticleForm(initial={'user': request.user})

    return render(request, 'writepost.html', {'form': form, 'tags':tags, 'user_profile':user_profile})

@login_required(login_url='login')
def updatearticle(request, id):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    tags = Tag.objects.all()
    article = get_object_or_404(Article, id=id)

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user  # Ensure the user is set
            article.save()
            form.save_m2m()
            return redirect('home')  # Redirect to a success page
    else:
        form = ArticleForm(instance=article)

    return render(request, 'writepost.html', {'form': form, 'tags': tags, 'user_profile': user_profile})

@login_required(login_url='login')
def deletearticle(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    
    if request.method == 'POST':
        article.delete()
        return redirect('home')  # Redirect to a success page

    return render(request, 'deletearticle.html', {'article': article})

@login_required(login_url='login')
def articleDetail(request, id):
    user_object = User.objects.get(username = request.user.username)
    user_profile = Profile.objects.get(user = user_object)
    article = Article.objects.get(id = id)
    comments = article.comments.all()
    form = CommentForm()
    tags = Tag.objects.all()
    if request.method == 'POST':
        # get the article by article_id
        # A comment form
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.article = article
            new_comment.username = request.user.username
            new_comment.save()
            return redirect('viewArticle', id=id)
        else:
            form = CommentForm()
    comments = Comment.objects.filter(article = article)
    
    return render(request, 'article_detail.html', {'article':article, 'form':form, 'tags':tags, 'comments':comments, 'user_profile':user_profile})

@login_required(login_url='login')
def likearticle(request):
    user = request.user
    article_id = request.GET.get('article_id')
    article = get_object_or_404(Article, id=article_id)

    # Check if the user has already liked the article
    like = LikeArticle.objects.filter(article=article, user=user).first()
    
    if like is None:
        # User hasn't liked the article yet
        LikeArticle.objects.create(article=article, user=user)
        article.no_of_claps += 1
    else:
        # User has already liked the article
        like.delete()
        article.no_of_claps -= 1
    
    article.save()
    
    # Redirect to the index page with an anchor to the article
    index_url = reverse('home')
    return redirect(f'{index_url}#article-{article.id}')

def searchArticle(request):
    user_object = User.objects.get(username = request.user.username)
    user_profile = Profile.objects.get(user = user_object)
     # Query all posts
    tags = Tag.objects.all()
    search_article = request.GET.get('search')
    if search_article:
        articles = Article.objects.filter(Q(title__icontains=search_article))
    else:
        # If not searched, return default posts
        articles = Article.objects.all().order_by("-created_on")
    return render(request, 'index.html', {'articles': articles, 'tags':tags, 'user_profile':user_profile})

    
def articlesByTag(request):
    tag = request.GET.get("tag")
    tags = Tag.objects.all()
    if (tag):
        articles = Article.objects.filter(tags__name__in=[tag]) #tags filtered by tag parameter
        return render(request, 'index.html', {'articles': articles, 'tags':tags})
    else:
        articles = Article.objects.all()
        return render(request, 'index.html', {'articles': articles, 'tags':tags})
    

def topArticles(request):
    user_object = User.objects.get(username = request.user.username)
    user_profile = Profile.objects.get(user = user_object)
    tags = Tag.objects.all()
    articles = Article.objects.order_by('-no_of_claps')
    return render(request, "index.html", {"articles": articles, 'tags':tags, 'user_profile':user_profile})


def newArticles(request):
    user_object = User.objects.get(username = request.user.username)
    user_profile = Profile.objects.get(user = user_object)
    tags = Tag.objects.all()
    articles = Article.objects.order_by('-created_on')
    return render(request, "index.html", {"articles": articles, 'tags':tags, 'user_profile':user_profile})

    