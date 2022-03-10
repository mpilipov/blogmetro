from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
# Create your models here.
class Post(models.Model):
    h1 = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    url_slug = models.SlugField(default='', null=False, db_index=True)
    descr = RichTextUploadingField()
    content = RichTextUploadingField()
    image = models.ImageField()
    created = models.DateField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE) # создание отношения между таблицами User и Post
    tag = TaggableManager(verbose_name='tag')

    def __str__(self):
        return self.title
    # Необходимо удалить при использовании prepopulated_fields()!
    #def save(self, *args, **kwargs):
     #   self.url_slug = slugify(self.title)
      #  super(Post, self).save(*args, **kwargs)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_name')
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.text