from django.urls import path
from .views import index, show_post

urlpatterns = [
  path('', index),
  path('post/<int:post_id>/', show_post, name='post'),
]
