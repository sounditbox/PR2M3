from config.settings import MEDIA_ROOT
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Avg, Min, Max, ProtectedError
from django.http import HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView, ListView, DetailView, DeleteView, \
    CreateView, UpdateView

from .forms import ContactForm, ArticleCreateForm, ArticleEditForm, CommentForm
from .models import Article, Comment


class SimpleView(LoginRequiredMixin, View):
    message = "Default message"

    def get(self, request, *args, **kwargs):
        return HttpResponse(self.message)


class AboutView(TemplateView):
    template_name = "posts/about.html"


# def upload_file(request):
#     if request.method == "POST":
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             handle_uploaded_file(request.FILES["file"])
#             return HttpResponseRedirect("/success/url/")
#     else:
#         form = UploadFileForm()
#     return render(request, "upload.html", {"form": form})


def handle_uploaded_file(f):
    with open(MEDIA_ROOT / f.name, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


class ArticleListView(ListView):
    model = Article
    template_name = "posts/article_list.html"
    context_object_name = "articles"
    paginate_by = 5

    def get_queryset(self):
        return (Article.objects
                .values('pk', 'title', 'content', 'views', 'author')
                .annotate(comments_count=Count('comments')))


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'posts/article_detail.html'
    context_object_name = 'article'

    def get_object(self, queryset=None):
        article = super().get_object(queryset)
        article.views += 1
        article.save(update_fields=['views'])
        return article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    context_object_name = 'article'
    template_name = 'posts/article_confirm_delete.html'
    success_url = reverse_lazy('posts:article_list')

    def form_valid(self, form):
        try:
            res = super().form_valid(form)
            messages.success(self.request,
                             f'Пост {self.object.pk} успешно удален!')
            return res
        except ProtectedError:
            messages.error(self.request,
                           f'Пост {self.object.pk} нельзя удалить, т.к. имеет связанные комментарии')
            return super().form_invalid(form)


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleCreateForm
    template_name = 'posts/article_create.html'
    extra_context = {'title': 'Новый пост'}

    def form_valid(self, form):
        messages.success(self.request, 'Пост успешно создан')
        form.instance.author = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Пост не создан')
        return super().form_invalid(form)


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleEditForm
    template_name = 'posts/article_edit.html'

    def form_valid(self, form):
        messages.success(self.request, 'Пост успешно обновлен')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Пост не обновлен')

        return super().form_invalid(form)


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    context_object_name = 'comment'
    template_name = 'posts/comment_confirm_delete.html'

    def form_valid(self, form):
        messages.success(self.request, 'Комментарий успешно удален')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('posts:article_detail', kwargs={'pk': self.object.article.pk})


@require_POST
@login_required
def create_comment(request: HttpRequest, pk: int) -> HttpResponse:
    article = get_object_or_404(Article, pk=pk)

    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.article = article
        comment.author = request.user
        comment.save()
        return redirect('posts:article_detail', pk=article.pk)

    return redirect('posts:article_detail', pk=article.pk)


@login_required
def stats(request: HttpRequest) -> HttpResponse:
    a_stats = Article.objects.aggregate(
        total_posts=Count('pk'),  # Общее количество постов
        avg_views=Avg('views'),  # Среднее количество просмотров
        min_views=Min('views'),  # Минимальное количество просмотров
        max_views=Max('views'),  # Максимальное количество просмотров
    )
    c_stats = Comment.objects.aggregate(
        total_comments=Count('pk'),  # Общее количество комментариев

    )
    a_stats.update(c_stats)
    return render(request, 'posts/stats.html', context=a_stats)


def contacts(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            messages.success(request, 'Спасибо за заявку!')
            return redirect('contacts')
        else:
            print(form.errors)
            messages.error(request, 'Заполните форму правильно!')
            return render(request, 'posts/contacts.html',
                          context={'form': form})

    context = {
        'title': 'Contacts',
        'form': ContactForm()
    }

    return render(request, 'posts/contacts.html', context=context)
