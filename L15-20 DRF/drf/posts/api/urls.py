from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from posts.api.views import CommentViewSet, TagViewSet, CategoryViewSet, \
    ArticleViewSet, SessionAuthView, ObtainAuthTokenView, UserViewSet

app_name = 'posts'

router = DefaultRouter()

router.register('comments', CommentViewSet)
router.register('tags', TagViewSet)
router.register('categories', CategoryViewSet)
router.register('articles', ArticleViewSet)
router.register('users', UserViewSet)

urlpatterns = router.urls + [
    path('session_auth/', SessionAuthView.as_view(), name='session_auth'),
    path('token_auth/', ObtainAuthTokenView.as_view(), name='token_auth'),

    # JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),

]
