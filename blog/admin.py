from django.contrib import admin
from .models import Post, Comment


# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ['h1', 'title', 'descr', 'image', 'created', 'author','url_slug']
    # list_editable = ['title', 'url_slug', 'descr', 'image', 'created', 'author', 'tag']
    # exclude=['url_slug']
    # Необходимо удалить метод save() из модели при использовании prepopulated_fields()!
    prepopulated_fields = {'url_slug': ('h1',)}


admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('username', 'post', 'text', 'created_date')
    #list_filter = ('username', 'created_date')
    #search_fields = ('username', 'text')
admin.site.register(Comment, CommentAdmin)