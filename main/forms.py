from django.forms import ModelForm
from main.models import Article
from django import forms

class ArticleForm(ModelForm):
    
    class Meta:
        model = Article
        fields = ["title", 'body', "image"]