from django.urls import path

from .views import (SimpleView, AboutView, ArticleListView, ArticleDetailView, \
    ArticleDeleteView, ArticleCreateView, ArticleUpdateView, CommentDeleteView,
                    create_comment, stats, contacts)

app_name = 'posts'

urlpatterns = [
    path('simple/', SimpleView.as_view(), name='simple'),
    path('about/', AboutView.as_view(), name='about'),
    path('contacts/', contacts, name='contacts'),
    path('articles/', ArticleListView.as_view(), name='article_list'),
    path(
        'articles/<int:pk>/',
        ArticleDetailView.as_view(),
        name='article_detail'
    ),
    path(
        'articles/delete/<int:pk>/',
        ArticleDeleteView.as_view(),
        name='article_delete'
    ),
    path(
        'articles/create/',
        ArticleCreateView.as_view(),
        name='article_create'
    ),
    path('articles/edit/<int:pk>/',
         ArticleUpdateView.as_view(),
         name='article_edit'),
    path('articles/<int:pk>/comment/', create_comment,
         name='comment_create'),
    path('comments/<int:pk>/delete/', CommentDeleteView.as_view(),
         name='comment_delete'),
    path('articles/stats/', stats, name='stats'),
]


# CRUD
