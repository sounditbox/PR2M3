from django.urls import path
from rest_framework.routers import DefaultRouter

from posts.api.views import CommentViewSet, TagViewSet, CategoryViewSet, \
    ArticleViewSet, SessionAuthView, ObtainAuthTokenView

app_name = 'posts'

router = DefaultRouter()
router.register('comments', CommentViewSet, basename='comments')
router.register('tags', TagViewSet, basename='tags')
router.register('categories', CategoryViewSet, basename='categories')
router.register('articles', ArticleViewSet, basename='articles')
urlpatterns = router.urls + [
    path('session_auth/', SessionAuthView.as_view(), name='session_auth'),
    path('token_auth/', ObtainAuthTokenView.as_view(), name='token_auth'),
]
