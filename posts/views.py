from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, viewsets, filters
from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import SessionAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post, Category, Tag
from .permissions import IsAuthorOrReadOnly
from .serializers import PostSerializer, CategorySerializer, TagSerializer, UserSerializer
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_page
from rest_framework.decorators import api_view
from django.core.cache import cache
from .models import Post

class PostViewSet(viewsets.ModelViewSet):
    queryset=Post.objects.all().order_by('-created_at')
    serializer_class=PostSerializer
    permission_classes=[IsAuthorOrReadOnly]
    authentication_classes=[SessionAuthentication]
    filter_backends=[filters.SearchFilter, DjangoFilterBackend]
    search_fields=['title','content','author__username']
    filterset_fields=['author','created_at']

    @api_view(['GET'])
    @cache_page(60*15)
    def list_posts(request):
        posts=Post.objects.all()
        serializer=PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    def get_statistics():
        stats=cache.get('my_stats_key')
        if not stats:
            print('Complex process...')
            count=Post.objects.count()
            stats={'total_posts':count, 'status':'active'}
            cache.set('my_stats_key', stats, 60*60)
        return stats

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer
    permission_classes=[IsAdminUser]
    authentication_classes=[SessionAuthentication]

    
class TagViewSet(viewsets.ModelViewSet):
    queryset=Tag.objects.all()
    serializer_class=TagSerializer
    permission_classes=[IsAdminUser]
    authentication_classes=[SessionAuthentication]
    

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializer