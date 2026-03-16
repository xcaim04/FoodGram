from django.contrib import admin
from .models import Post, Like, Comment, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('emoji', 'name')
    search_fields = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('food_name', 'user', 'category', 'location', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('food_name', 'caption', 'user__username')
    raw_id_fields = ('user',)
    date_hierarchy = 'created_at'


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'text', 'created_at')
    search_fields = ('text', 'user__username')
