from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, \
    IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from posts.models import Comment, Category, Tag, Article
from .permissions import IsAuthorOrReadOnly, IsReadOnly, NoDelete
from .serializers import CommentSerializer, CategorySerializer, TagSerializer, \
    ArticleSerializer


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser | IsReadOnly, NoDelete]


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminUser | IsReadOnly]


class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.prefetch_related('tags', 'category')
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthorOrReadOnly, ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class SessionAuthView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response(
                {'status': 'error', 'message': 'Email and password required'},
                status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=email, password=password)
        if not user:
            return Response(
                {'status': 'error', 'message': 'Email or password invalid'},
                status=status.HTTP_400_BAD_REQUEST)
        # SessionID in cookie
        login(request, user)
        return Response({'status': 'success'})


class ObtainAuthTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response(
                {'status': 'error', 'message': 'Email and password required'},
                status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=email, password=password)
        if not user:
            return Response(
                {'status': 'error', 'message': 'Email or password invalid'},
                status=status.HTTP_400_BAD_REQUEST)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})
