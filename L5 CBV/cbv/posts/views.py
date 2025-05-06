from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, DeleteView, \
    CreateView, UpdateView

from .models import Article


class SimpleView(View):
    message = "Default message"

    def get(self, request, *args, **kwargs):
        return HttpResponse(self.message)


class AboutView(TemplateView):
    template_name = "posts/about.html"


class ArticleListView(ListView):
    model = Article
    template_name = "posts/article_list.html"
    context_object_name = "articles"

    # queryset = Article.objects.filter(is_published=True)
    # paginate_by = 5


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'posts/article_detail.html'
    context_object_name = 'article'


class ArticleDeleteView(DeleteView):
    model = Article
    context_object_name = 'article'
    template_name = 'posts/article_confirm_delete.html'
    success_url = reverse_lazy('article_list')


class ArticleCreateView(CreateView):
    model = Article
    template_name = 'posts/article_create.html'
    fields = ['title', 'content', 'is_published']


class ArticleUpdateView(UpdateView):
    model = Article
    template_name = 'posts/article_edit.html'
    fields = ['title', 'content', 'is_published']
