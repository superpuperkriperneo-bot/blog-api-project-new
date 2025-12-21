from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    tag_name=models.CharField(max_length=100,unique=True ,verbose_name='tag_name')

class Category(models.Model):
    category_name=models.CharField(max_length=100, unique=True, verbose_name='Category')

class Post(models.Model):
    author=models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='author', related_name='posts')
    category=models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='category', related_name='posts')
    title=models.CharField(max_length=200, verbose_name='title')
    content=models.TextField(verbose_name='content')
    tags=models.ManyToManyField(Tag, blank=True, verbose_name="tags", related_name="posts")
    is_published=models.BooleanField(default=False, verbose_name='is_published')
    updated_at=models.DateTimeField(auto_now=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

