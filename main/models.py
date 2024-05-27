from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from django.contrib.auth import get_user_model

User  = get_user_model()

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')
    id_user = models.IntegerField()
    profileimg = models.ImageField(upload_to='images/', default='default-user-pic.webp')
    
    def __str__(self):
        return self.user.username

class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    body = RichTextUploadingField()
    image = models.ImageField(upload_to="images/", default=None) 
    created_on = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager(help_text="Select tag")
    no_of_claps = models.IntegerField(default=0)
    
    def __str__(self):
       return self.title
   
class LikeArticle(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    username = models.CharField(max_length=100, blank=True, default=None)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]
    
    def __str__(self):
        return f'Comment by {self.username} on {self.article}'