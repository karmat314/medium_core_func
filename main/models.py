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