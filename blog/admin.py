from django.contrib import admin
from .models import Post, Category, Tag, Comment


admin.site.register(Post)


class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'content', 'created_at']
    list_filter = ['created_at', 'author']
    search_fields = ['content', 'author__username']


admin.site.register(Comment, CommentAdmin)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}


admin.site.register(Category, CategoryAdmin)


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}


admin.site.register(Tag, TagAdmin)
