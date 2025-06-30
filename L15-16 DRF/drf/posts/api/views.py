from rest_framework.viewsets import ModelViewSet

from posts.models import Comment, Category, Tag, Article
from .serializers import CommentSerializer, CategorySerializer, TagSerializer, \
    ArticleSerializer


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.prefetch_related('tags', 'category')
    serializer_class = ArticleSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
