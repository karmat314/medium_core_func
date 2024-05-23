from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import ArticleForm
from .models import Article
# Create your views here.
def index(request):
    articles = Article.objects.all()
    return render(request, "index.html", {"articles": articles})

def writepost(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=True)
            return redirect('home')
        else:
            return HttpResponse('You fucked up!')
    return render(request, 'writepost.html', {'form':ArticleForm})

def articleDetail(request, id):
    article = Article.objects.get(id = id)
    return render(request, 'article_detail.html', {'article':article})