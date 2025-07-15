from django.contrib.auth import authenticate, login, get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import CreateAPIView, ListAPIView, \
    ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticatedOrReadOnly,
    IsAdminUser
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from posts.models import Comment, Category, Tag, Article
from .filters import ArticleFilter
from .permissions import IsAuthorOrReadOnly, IsReadOnly, NoDelete, IsAdminOrSelf
from .serializers import (
    CommentSerializer,
    CategorySerializer,
    TagSerializer,
    ArticleSerializer, AuthorSerializer, PasswordSerializer
)


class DefaultPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 5


class CategoryCreateView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.select_related('article', 'author')
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    search_fields = ['content',
                     '=author__username']
    ordering_fields = ['title', 'views', 'created_at']
    ordering = ['-created_at']
    filterset_fields = ['article', 'author']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser | IsReadOnly, NoDelete]
    pagination_class = DefaultPagination


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminUser | IsReadOnly]
    pagination_class = DefaultPagination


class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.prefetch_related('tags', 'category').select_related('author')
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthorOrReadOnly, ]
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title', 'content',
                     '=author__username',
                     '^author__email']
    ordering_fields = ['title', 'views', 'created_at']
    ordering = ['-created_at']
    filterset_class = ArticleFilter

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


class UserViewSet(ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = get_user_model().objects.all()
    serializer_class = AuthorSerializer

    @action(detail=True, methods=['post'], permission_classes=[IsAdminOrSelf])
    def set_password(self, request, pk=None):
        user = self.get_object()
        serializer = PasswordSerializer(data=request.data, context={'user': user})
        if serializer.is_valid():
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False)
    def recent_users(self, request):
        recent_users = get_user_model().objects.all().order_by('-last_login')

        page = self.paginate_queryset(recent_users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(recent_users, many=True)
        return Response(serializer.data)