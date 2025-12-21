from rest_framework import serializers
from .models import  Category, Post, User, Tag

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','first_name','last_name')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id','tag_name')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','category_name')


class PostSerializer(serializers.ModelSerializer):

    author = UserSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='author', write_only=True, required=False)

    category=CategorySerializer(read_only=True)
    category_id=serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True, required=False ,allow_null=True)

    tags=TagSerializer(read_only=True, many=True)
    tag_id=serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, source='tags', write_only=True, required=False)

    class Meta:
        model = Post
        fields = ('id',
                'category','category_id',
                'author','author_id',
                'title',
                'content',
                'tags','tag_id',
                'created_at',
                'is_published')