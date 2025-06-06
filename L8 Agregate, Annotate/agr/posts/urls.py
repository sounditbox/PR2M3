from django.urls import path

from .views import SimpleView, AboutView, ArticleListView, ArticleDetailView, \
    ArticleDeleteView, ArticleCreateView, ArticleUpdateView, create_comment, stats

urlpatterns = [
    path('simple/', SimpleView.as_view(), name='simple'),
    path('about/', AboutView.as_view(), name='about'),
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
    path('articles/<int:pk>/comment/', create_comment, name='comment_create'),
    path('articles/stats/', stats, name='stats'),
]

# CRUD
