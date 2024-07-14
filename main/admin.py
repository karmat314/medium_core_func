from django.contrib import admin

# Register your models here.
from .models import Article, Comment, Profile, LikeArticle


class ArticleAdmin(admin.ModelAdmin):
    # Specify which fields to display in the list view
    list_display = ('title', 'user', 'created_on', 'no_of_claps')
    
    # Add filters for the sidebar
    list_filter = ('created_on', 'tags')
    
    # Add search functionality
    search_fields = ('title', 'body')
    
    # Automatically fill the created_on field
    readonly_fields = ('created_on',)
    
    # Customize the form layout
    fieldsets = (
        (None, {
            'fields': ('user', 'title', 'body', 'image', 'tags', 'no_of_claps')
        }),
        ('Important dates', {
            'fields': ('created_on',)
        }),
    )

# Register the model with the customized admin class
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(LikeArticle)