from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=300)
    body = RichTextUploadingField()
    image = models.ImageField(upload_to="images/", default=None) 
    created_on = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager(help_text="Select tag")
   
    def __str__(self):
       return self.title

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    username = models.CharField(max_length=100)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]
    
    def __str__(self):
        return f'Comment by {self.username} on {self.article}'