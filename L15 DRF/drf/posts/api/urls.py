from django.urls import path
from rest_framework.routers import DefaultRouter

from posts.api.views import CommentViewSet

app_name = 'posts'

router = DefaultRouter()
router.register('comments', CommentViewSet, basename='comments')

urlpatterns = router.urls
