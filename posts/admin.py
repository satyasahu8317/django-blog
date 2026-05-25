# pyrefly: ignore [missing-import]
from django.contrib import admin
from .models import Post, Category, Comment
# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title','slug','author','publish','status')
    list_filter = ('status','publish','author')
    search_fields = ('title','body')
    prepopulated_fields = {'slug':('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')
   


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

# ... (keep your PostAdmin code below)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email','post', 'created', 'active')
    list_filter = ('active', 'created')
    search_fields = ('name', 'email', 'body')